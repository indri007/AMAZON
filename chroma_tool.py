from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import chromadb
from chromadb.utils import embedding_functions

DB_DIR = Path(".chromadb")
COLLECTION_HRD = "hrd_docs"
COLLECTION_MRC = "idk_mrc_qa"


def chunk_text(text: str, chunk_size: int = 160, overlap: int = 30) -> List[str]:
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


def load_qa_training_data(folder: Path) -> List[Dict[str, str]]:
    docs: List[Dict[str, str]] = []
    for json_file in ["idk_mrc_test.json", "idk_mrc_valid.json"]:
        path = folder / json_file
        if path.exists():
            try:
                items = json.loads(path.read_text(encoding="utf-8"))
                for idx, item in enumerate(items):
                    context = item.get("context", "")
                    qas = item.get("qas", [])
                    qa_texts = []
                    for q in qas:
                        question = q.get("question", "")
                        answers = [a.get("text", "") for a in q.get("answers", [])]
                        ans_str = ", ".join(answers) if answers else "[Tidak terjawab]"
                        qa_texts.append(f"Q: {question} -> A: {ans_str}")
                    
                    combined = f"Konteks: {context}\n" + "\n".join(qa_texts)
                    docs.append({
                        "id": f"{json_file}#{idx}",
                        "text": combined,
                        "source": f"training/{json_file}"
                    })
            except Exception as e:
                print(f"Warning: gagal membaca {path}: {e}")
    return docs


def get_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=str(DB_DIR))


def ingest_all(source_folder: Path) -> None:
    print("=" * 70)
    print("🧠 MEMULAI INGESTI & PELATIHAN DUAL-COLLECTION CHROMADB")
    print("=" * 70)

    client = get_client()
    embed = embedding_functions.DefaultEmbeddingFunction()

    # 1. INGEST COLLECTION 1: HRD KNOWLEDGE BASE
    print("\n[1/2] Memproses Dokumen Pengetahuan HRD...")
    hr_docs = load_md_documents(source_folder)
    print(f"📄 File Markdown ditemukan: {len(hr_docs)} file")

    try:
        client.delete_collection(COLLECTION_HRD)
    except Exception:
        pass
    col_hrd = client.create_collection(name=COLLECTION_HRD, embedding_function=embed)

    ids_hr, texts_hr, metas_hr = [], [], []
    for doc in hr_docs:
        chunks = chunk_text(doc["text"], chunk_size=150, overlap=30)
        for idx, chunk in enumerate(chunks, start=1):
            ids_hr.append(f"{doc['id']}#{idx}")
            texts_hr.append(chunk)
            metas_hr.append({"source": doc["source"], "chunk": str(idx), "category": "HR_Policy"})

    col_hrd.add(ids=ids_hr, documents=texts_hr, metadatas=metas_hr)
    print(f"✅ Collection '{COLLECTION_HRD}' selesai: {len(ids_hr)} chunks tersimpan!")

    # 2. INGEST COLLECTION 2: IDK-MRC QA DATASET
    print("\n[2/2] Memproses Korpus QA Bahasa Indonesia (IDK-MRC)...")
    qa_docs = load_qa_training_data(Path("training/data"))
    print(f"📚 Sampel QA ditemukan: {len(qa_docs)} sampel")

    try:
        client.delete_collection(COLLECTION_MRC)
    except Exception:
        pass
    col_mrc = client.create_collection(name=COLLECTION_MRC, embedding_function=embed)

    ids_mrc, texts_mrc, metas_mrc = [], [], []
    for doc in qa_docs:
        ids_mrc.append(doc["id"])
        texts_mrc.append(doc["text"])
        metas_mrc.append({"source": doc["source"], "category": "Indonesian_MRC"})

    # Batch add for QA dataset
    batch_size = 100
    for i in range(0, len(ids_mrc), batch_size):
        end = min(i + batch_size, len(ids_mrc))
        col_mrc.add(ids=ids_mrc[i:end], documents=texts_mrc[i:end], metadatas=metas_mrc[i:end])

    print(f"✅ Collection '{COLLECTION_MRC}' selesai: {len(ids_mrc)} QA contexts tersimpan!")
    print("\n" + "=" * 70)
    print(f"🎉 SUKSES! Total {len(ids_hr) + len(ids_mrc)} aset vektor tersimpan di {DB_DIR}")
    print("=" * 70)


def query_docs(query: str, collection_name: str = COLLECTION_HRD, top_k: int = 3) -> None:
    client = get_client()
    embed = embedding_functions.DefaultEmbeddingFunction()
    try:
        collection = client.get_collection(collection_name, embedding_function=embed)
    except Exception:
        raise SystemExit(
            f"Collection '{collection_name}' tidak ditemukan. Jalankan dulu: python chroma_tool.py ingest"
        )

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=['metadatas', 'documents'],
    )

    if not results["documents"] or not results["documents"][0]:
        print("Tidak ada hasil untuk query ini.")
        return

    print(f"\n🔎 Top {top_k} hasil pencarian vektor di '{collection_name}' untuk: '{query}'")
    print("-" * 70)
    for index, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0]), start=1):
        source = meta.get("source", "-")
        chunk = meta.get("chunk", "-")
        print(f"[{index}] Sumber: {source} (Chunk: {chunk})")
        snippet = doc[:300] + ("..." if len(doc) > 300 else "")
        print(f"    {snippet}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tool vector store lokal berbasis Chroma")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Ingest seluruh dokumen dan korpus pelatihan")
    ingest_parser.add_argument(
        "--docs",
        type=Path,
        default=Path("hrd-docs"),
        help="Folder dokumen sumber (default: hrd-docs)",
    )

    query_parser = subparsers.add_parser("query", help="Cari dokumen relevan dengan query")
    query_parser.add_argument("query", type=str, help="Teks query pencarian")
    query_parser.add_argument(
        "--collection",
        type=str,
        default=COLLECTION_HRD,
        choices=[COLLECTION_HRD, COLLECTION_MRC],
        help=f"Target collection (default: {COLLECTION_HRD})",
    )
    query_parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Jumlah hasil teratas yang ditampilkan (default: 3)",
    )

    args = parser.parse_args()

    if args.command == "ingest":
        ingest_all(args.docs)
    elif args.command == "query":
        query_docs(args.query, collection_name=args.collection, top_k=args.top_k)


if __name__ == "__main__":
    main()
