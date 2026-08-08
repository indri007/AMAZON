from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

DB_DIR = Path(".chromadb")
COLLECTION_NAME = "hrd_docs"


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100) -> List[str]:
    tokens: List[str] = text.split()
    if not tokens:
        return []

    chunks: List[str] = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk = " ".join(tokens[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def load_md_documents(folder: Path) -> List[Dict[str, str]]:
    docs: List[Dict[str, str]] = []
    for path in sorted(folder.rglob("*.md")):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            docs.append({
                "id": str(path.relative_to(folder)),
                "text": text,
                "source": str(path.relative_to(folder)),
            })
    return docs


def get_client() -> chromadb.Client:
    return chromadb.Client(
        Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(DB_DIR),
        )
    )


def ingest_docs(source_folder: Path, chunk_size: int, overlap: int) -> None:
    documents = load_md_documents(source_folder)
    if not documents:
        raise SystemExit(f"Tidak ditemukan file Markdown di: {source_folder}")

    embed = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    client = get_client()

    if COLLECTION_NAME in [col.name for col in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed,
    )

    ids: List[str] = []
    documents_to_add: List[str] = []
    metadatas: List[Dict[str, str]] = []

    for doc in documents:
        chunks = chunk_text(doc["text"], chunk_size=chunk_size, overlap=overlap)
        for index, chunk in enumerate(chunks, start=1):
            ids.append(f"{doc['id']}#{index}")
            documents_to_add.append(chunk)
            metadatas.append({"source": doc["source"], "chunk": str(index)})

    collection.add(
        ids=ids,
        documents=documents_to_add,
        metadatas=metadatas,
    )
    client.persist()
    print(f"✅ Ingest selesai. {len(ids)} chunk tersimpan di collection '{COLLECTION_NAME}'.")


def query_docs(query: str, top_k: int) -> None:
    client = get_client()
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except ValueError:
        raise SystemExit(
            f"Database tidak ditemukan. Jalankan dulu: python chroma_tool.py ingest"
        )

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=['metadatas', 'documents'],
    )

    if not results["documents"] or not results["documents"][0]:
        print("Tidak ada hasil untuk query ini.")
        return

    print(f"🔎 Top {top_k} hasil:")
    for idx, (doc, metadata) in enumerate(
        zip(results["documents"][0], results["metadatas"][0]), start=1
    ):
        print("---")
        print(f"[{idx}] sumber: {metadata.get('source')} chunk: {metadata.get('chunk')}")
        print(doc)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chroma local tool untuk ingest dan query dokumen HRD"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Ingest seluruh file Markdown ke Chroma")
    ingest_parser.add_argument(
        "--docs", default="hrd-docs", help="Folder dokumen HRD"
    )
    ingest_parser.add_argument(
        "--chunk-size", type=int, default=700, help="Ukuran maksimum token per chunk"
    )
    ingest_parser.add_argument(
        "--overlap", type=int, default=100, help="Overlap token antar chunk"
    )

    query_parser = subparsers.add_parser("query", help="Query local Chroma collection")
    query_parser.add_argument("query", help="Query yang ingin dijalankan")
    query_parser.add_argument("--top-k", type=int, default=5, help="Jumlah hasil teratas")

    args = parser.parse_args()

    if args.command == "ingest":
        ingest_docs(Path(args.docs), args.chunk_size, args.overlap)
    elif args.command == "query":
        query_docs(args.query, args.top_k)


if __name__ == "__main__":
    main()
