# Persistence Plan untuk Langflow + Vector Store di Cloud Run

## Tujuan
Memastikan Langflow Cloud Run dapat menyimpan dan memuat kembali vector store secara konsisten setelah container restart, deploy ulang, atau scaling.

## Masalah saat ini
- Cloud Run container filesystem bersifat ephemeral.
- Chroma / DuckDB file yang berada di local disk tidak bertahan antar instance.
- Dokumentasi repo belum menjelaskan persistence yang stabil untuk vector store.

## Opsi persistence

### 1. Chroma dengan DuckDB+Parquet di Cloud Run + Persistent Volume

**Kelebihan**
- Simpel jika menggunakan storage lokal yang dipetakan persisten.
- Data tetap ada setelah restart.

**Kekurangan**
- Cloud Run standar tidak mendukung persistent volume lokal selain `/tmp`.
- Butuh solusi tambahan seperti Cloud Run for Anthos atau GKE/GKE Autopilot.

**Rekomendasi**
- Gunakan `chromadb` dengan backend `duckdb+parquet` hanya untuk eksperimen lokal.
- Untuk Cloud Run produksi, gunakan alternatif storage remote.

### 2. Chroma dengan Cloud Storage / GCS

**Kelebihan**
- Memanfaatkan Google Cloud Storage sebagai tempat file `.parquet`.
- Lebih cocok untuk Cloud Run karena storage eksternal.

**Kekurangan**
- Performa query lebih lambat dibanding local disk.
- Perlu integrasi custom untuk load/save file.

**Implementasi**
- Simpan file Chroma/DB ke bucket GCS.
- Setiap container Cloud Run mount atau download file sebelum start.
- Persist kembali saat shutdown atau update data.

### 3. Chroma Server terpisah / vector DB terkelola

**Kelebihan**
- Arsitektur paling stabil untuk produksi.
- Database terpisah tidak bergantung pada lifecycle Cloud Run.

**Pilihan**
- Chroma Enterprise / open-source server
- Milvus
- Pinecone
- Qdrant
- Weaviate

**Rekomendasi**
- Pilih Chroma server atau DB terkelola jika kamu butuh persistence + performa.
- Gunakan Cloud Run hanya sebagai Langflow backend, sedangkan vector store dikelola di service terpisah.

## Rencana implementasi yang paling cocok

### A. Gunakan Langflow Cloud Run + Chroma eksternal

1. Deploy Langflow di Cloud Run.
2. Pastikan Langflow menggunakan dependency `langchain_chroma` dan `chromadb`.
3. Konfigurasi Knowledge node di Langflow agar backend `langchain_chroma`.
4. Simpan vector store di Chroma server eksternal atau DB terpisah.
5. Atur `GEMINI_API_KEY` di Global Variables.
6. Lakukan ingest dokumen di langflow.
7. Verifikasi retrieval setelah restart.

### B. Gunakan Chroma lokal untuk development/eksperimen

1. Jalankan `chroma_tool.py ingest --docs hrd-docs`.
2. Simpan file `.chromadb/` di local disk.
3. Gunakan `python chroma_tool.py query "..."` untuk validasi.
4. Tidak cocok untuk produksi Cloud Run.

## Checklist verifikasi produksi

- [ ] `GEMINI_API_KEY` sudah di-set di Cloud Run env variables.
- [ ] Langflow Cloud Run dapat ingest dokumen tanpa error.
- [ ] Vector store persistent di luar lifecycle container.
- [ ] Query retrieval menghasilkan konteks yang benar setelah restart.
- [ ] Backup bucket / storage sudah tersedia untuk vector store.
- [ ] MCP endpoint tetap valid setelah deploy ulang.

## Catatan tambahan

- Jika ingin tetap di Cloud Run dan tidak ingin mengelola DB terpisah, gunakan solusi serverless yang menyimpan state di storage remote.
- Untuk audit PRD, fokus pada persistence, API key naming, dan flow runtime yang bisa diulang.
