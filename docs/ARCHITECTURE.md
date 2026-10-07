# Arsitektur Saat Ini

## Ringkasan

Project ini saat ini berjalan sebagai integrasi antara:
- Streamlit frontend (`streamlit_app.py`) untuk UI chatbot HRD,
- Langflow backend yang dideploy di Google Cloud Run,
- Flow Langflow `langflow/Vector Store RAG.json` untuk pipeline RAG,
- Optional: IBM Bob melalui MCP proxy untuk akses tool.

Dokumentasi ini mencerminkan keadaan saat ini, termasuk naming env var, arsitektur data flow, dan status persistence vector store.

## Diagram Arsitektur (ASCII)

```
User Browser
     │
     ▼
Streamlit Cloud App
(streamlit_app.py)
     │ HTTP POST /api/v1/run/{FLOW_ID}
     │ x-api-key: LANGFLOW_API_KEY
     ▼
Langflow Cloud Run
(Google Cloud Run)
     │
     ├─ Knowledge (Vector Store / RAG)
     │
     ├─ EmbeddingModel (gemini-embedding-2)
     │
     ├─ Agent + Prompt + Parser
     │
     └─ Chat Output

Optional:
IBM Bob → uvx mcp-proxy → Langflow MCP Endpoint

Note: Provider key for embedding is GEMINI_API_KEY, separate from frontend LANGFLOW_API_KEY.
```

## Komponen Utama

1. **Streamlit App**
   - File: `streamlit_app.py`
   - Menggunakan secrets:
     - `LANGFLOW_URL`
     - `FLOW_ID`
     - `LANGFLOW_API_KEY`
   - Menyusun request ke Langflow API:
     - `POST {LANGFLOW_URL}/api/v1/run/{FLOW_ID}?stream=false`
     - Header: `x-api-key: {LANGFLOW_API_KEY}`

2. **Langflow Cloud Run**
   - Service: `langflow` di region `asia-southeast2`
   - Endpoint publik: `https://langflow-192433070716.asia-southeast2.run.app`
   - Environment variable yang dicari oleh `check_env.py`: `GEMINI_API_KEY`
   - Flow yang dipakai: `Vector Store RAG` (flow ID `d8eedd75-92a7-47f0-974a-b74c0062ea23`)

3. **Flow Langflow**
   - File: `langflow/Vector Store RAG.json`
   - Komponen inti:
     - `Knowledge` (mode: Ingest / Retrieve)
     - `EmbeddingModel` (provider: Gemini embedding)
     - `Agent` (LLM generator)
     - `Prompt Template`
     - `Parser`
     - `Chat Output`
   - Embedding dimensi: 3072
   - Backend vector store saat ini belum diverifikasi secara persisten di Cloud Run.

4. **IBM Bob (opsional)**
   - File contoh: `.bob/mcp.json.example`
   - Konfigurasi MCP proxy:
     - lokal: `http://localhost:7862/api/v1/mcp/project/05688c3b-4f2e-4b3e-995d-933594bd00c3/streamable`
     - Cloud Run: `https://langflow-192433070716.asia-southeast2.run.app/api/v1/mcp/project/a2a1a234-0b47-4007-a4e7-1d8fec7b3ebf/streamable`
   - `x-api-key` digunakan untuk otentikasi.

## Alur Data Saat Ini

1. Pengguna mengetik pertanyaan di Streamlit.
2. `streamlit_app.py` mengirim request ke Langflow Cloud Run via API `run/{FLOW_ID}`.
3. Langflow menjalankan flow `Vector Store RAG`.
4. `Knowledge` melakukan retrieval dari knowledge base / vector store.
5. `EmbeddingModel` membuat embeddings jika diperlukan.
6. Agent memproses konteks + prompt untuk menghasilkan jawaban.
7. Jawaban dikembalikan ke Streamlit untuk ditampilkan.

## Status Persistence Vector Store

- Saat ini belum ada verifikasi persistence yang lengkap untuk vector store di Cloud Run.
- `PERSISTENCE_PLAN.md` telah dibuat untuk menjelaskan opsi persistence.
- Jika ingin produksi stabil, gunakan backend persistent seperti:
  - Chroma dengan external storage,
  - Chroma server terpisah,
  - atau layanan vector DB terkelola.

## Catatan Khusus

- `langflow/Vector Store RAG.json` berisi internal field `api_key: "google_api_key"` dalam flow metadata.
  - Ini tidak berarti `GOOGLE_API_KEY` masih dipakai sebagai env var di deployment.
  - Config runtime saat ini harus menggunakan `GEMINI_API_KEY` di Langflow Cloud Run.

- `streamlit_app.py` memisahkan env var frontend (`LANGFLOW_API_KEY`) dari backend provider key (`GEMINI_API_KEY`).

## Kesimpulan

Arsitektur saat ini adalah:

- Frontend: Streamlit Cloud
- Backend: Langflow Cloud Run
- Flow: `Vector Store RAG`
- Auth: `LANGFLOW_API_KEY` untuk Langflow API, `GEMINI_API_KEY` untuk provider embedding
- Persistence: belum terverifikasi untuk vector store di Cloud Run
