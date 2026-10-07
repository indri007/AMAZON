# ERD Project Langflow-Bob

Dokumen ini menggambarkan entitas data utama dan hubungan di dalam project `langflow-bob`.
ERD difokuskan pada arsitektur chat HRD, aliran data antara frontend, Langflow, dan vector store.

## Entitas dan Hubungan

- `User`
  - representasi pengguna akhir yang berinteraksi dengan aplikasi Streamlit.
  - berhubungan dengan satu atau lebih `ChatSession`.

- `ChatSession`
  - sesi percakapan yang dibuat per pengguna atau per kunjungan browser.
  - menyimpan `session_id` di `streamlit_app.py` menggunakan `st.session_state`.
  - berisi satu atau lebih `Message`.
  - terkait dengan satu `LangflowFlow` yang digunakan untuk memproses permintaan.

- `Message`
  - setiap entri percakapan dari pengguna (`user`) atau dari assistant (`assistant`).
  - atribut penting: `role`, `content`, `timestamp` (implisit), `session_id`.

- `LangflowFlow`
  - flow RAG Langflow yang didefinisikan di `langflow/Vector Store RAG.json`.
  - bertindak sebagai pipeline untuk ingest, retrieval, prompt, dan agent generation.
  - menerima input dari `Streamlit App` melalui API `POST /api/v1/run/{FLOW_ID}`.

- `KnowledgeDocument`
  - dokumen sumber HRD yang berasal dari folder `hrd-docs/`.
  - di-ingest ke `VectorStore`.
  - menyimpan metadata seperti nama file, jenis dokumen, dan teks sumber.

- `VectorStoreEntry`
  - representasi embedding dari `KnowledgeDocument`.
  - dihasilkan oleh `EmbeddingModel` (`gemini-embedding-2`).
  - digunakan untuk retrieval saat `LangflowFlow` menjalankan RAG.

- `APIRequest`
  - panggilan HTTP dari Streamlit ke Langflow.
  - membawa `input_value`, `session_id`, `output_type`, dan `input_type`.
  - autentikasi dengan header `x-api-key` menggunakan `LANGFLOW_API_KEY`.

## ERD Ringkas (ASCII)

```
+---------+           1       *           +-------------+
|  User   |-----------------------------| ChatSession |
+---------+                             +-------------+
      |                                       |
      | 1                                     | *
      |                                       |
      |                                   +-------+
      |                                   |Message|
      |                                   +-------+
      |                                       |
      |                                       |
      |                                       |
      |                                       v
      |                                 +----------------+
      |                                 | APIRequest     |
      |                                 +----------------+
      |                                         |
      |                                         |
      |                                         v
      |                                 +----------------+
      |                                 | LangflowFlow   |
      |                                 +----------------+
      |                                         |
      |                                         |
      |                                         v
      |                                +------------------+
      |                                | VectorStoreEntry |
      |                                +------------------+
      |                                         |
      |                                         |
      |        *                                |
      +-----------------------------------------+
                                           1
                                      +------------------+
                                      | KnowledgeDocument|
                                      +------------------+
```

## Keterangan Hubungan

- `User` 1..* `ChatSession`
  - satu pengguna bisa membuat banyak sesi percakapan.

- `ChatSession` 1..* `Message`
  - setiap sesi berisi riwayat pesan dari user dan assistant.

- `ChatSession` 1 `APIRequest`
  - setiap aksi chat di Streamlit memicu permintaan ke Langflow.

- `APIRequest` 1 `LangflowFlow`
  - request dikirim ke flow RAG yang benar berdasarkan `FLOW_ID`.

- `LangflowFlow` * `VectorStoreEntry`
  - flow dapat mencari banyak entri vector store untuk merespon satu query.

- `VectorStoreEntry` * `KnowledgeDocument`
  - setiap entry embedding berasal dari dokumen HRD sumber.

## Catatan Implementasi

- `ChatSession` tidak disimpan dalam database formal; hanya dikelola di `st.session_state` selama sesi Streamlit.
- `KnowledgeDocument` adalah dokumen Markdown di `hrd-docs/`.
- `VectorStoreEntry` saat ini belum memiliki persistence produksi yang terverifikasi di Cloud Run.
- `LangflowFlow` config berada di `langflow/Vector Store RAG.json` dan bergantung pada env var `GEMINI_API_KEY` untuk provider embedding.
- `Streamlit App` menggunakan env var `LANGFLOW_API_KEY` untuk memanggil Langflow API.

## Rekomendasi

- Jika ingin menambah persistence formal, tangkap `ChatSession` dan `Message` ke database terpisah.
- Pastikan `VectorStoreEntry` disimpan di backend yang mendukung restart kontainer.
- Gunakan diagram ini sebagai referensi untuk pengembangan data layer berikutnya.
