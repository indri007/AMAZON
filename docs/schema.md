# Schema Project Langflow-Bob

Dokumen ini menjelaskan schema utama untuk project ini berdasarkan kondisi repo saat ini.
Schema mencakup struktur file, konfigurasi environment, API request/response, serta hubungan antara komponen frontend, backend Langflow, dan vector store.

## 1. Struktur Repository

```
langflow-bob/
├── .bob/
│   └── mcp.json            # Konfigurasi MCP untuk IBM Bob
├── hrd-docs/               # Sumber dokumentasi HRD untuk ingest/retrieval
│   ├── faq_hrd.md
│   ├── Dokumentasi_Scope_*.md
│   └── prompts/
│       ├── agent1_router.md
│       ├── agent2_query_reformulation.md
│       ├── agent3_retrieval_grounding.md
│       ├── agent4_cs_responder.md
│       ├── agent5_hrd_interviewer.md
│       └── agent6_evaluator.md
├── langflow/
│   └── Vector Store RAG.json  # Flow Langflow untuk pipeline RAG
├── ARCHITECTURE.md
├── PERSISTENCE_PLAN.md
├── README.md
├── chroma_tool.py
├── check_env.py
├── design.md
├── requirements.txt
└── streamlit_app.py
```

## 2. Konfigurasi Environment

### 2.1 Streamlit App (`streamlit_app.py`)

`streamlit_app.py` mengharapkan secrets berikut:

- `LANGFLOW_URL`: URL endpoint Langflow, default `http://localhost:7862`
- `FLOW_ID`: ID flow Langflow yang dipanggil
- `LANGFLOW_API_KEY`: API key untuk otentikasi request ke Langflow

Contoh request:

```python
LANGFLOW_API = f"{LANGFLOW_URL}/api/v1/run/{FLOW_ID}?stream=false"
headers = {"Content-Type": "application/json"}
headers["x-api-key"] = API_KEY
```

Payload request:

```json
{
  "input_value": "<pertanyaan>",
  "output_type": "chat",
  "input_type": "chat",
  "session_id": "<uuid-session>"
}
```

### 2.2 Langflow Cloud Run

Langflow Cloud Run harus mengatur env var provider:

- `GEMINI_API_KEY`: API key Google Gemini untuk embedding / model provider

### 2.3 IBM Bob / MCP

Config MCP (`.bob/mcp.json`) akan menggunakan:

- `x-api-key`: API key untuk Langflow
- endpoint MCP Langflow, contohnya:
  - `https://langflow-192433070716.asia-southeast2.run.app/api/v1/mcp/project/.../streamable`

## 3. Schema API dan Data Flow

### 3.1 Frontend ke Langflow

Endpoint:

- `POST {LANGFLOW_URL}/api/v1/run/{FLOW_ID}?stream=false`

Headers:

- `Content-Type: application/json`
- `x-api-key: {LANGFLOW_API_KEY}`

Body:

```json
{
  "input_value": "<pertanyaan pengguna>",
  "output_type": "chat",
  "input_type": "chat",
  "session_id": "<uuid>"
}
```

Response yang diharapkan (`streamlit_app.py` mencari teks):

```json
{
  "outputs": [
    {
      "outputs": [
        {
          "results": {
            "message": {
              "text": "<jawaban>"
            }
          }
        }
      ]
    }
  ]
}
```

Jika respons tidak memiliki teks, aplikasi mengembalikan pesan fallback:

- `Maaf, tidak ada respons dari sistem.`
- `❌ Tidak dapat terhubung ke Langflow...`
- `❌ Waktu permintaan habis...`

### 3.2 Langflow Flow

Flow `langflow/Vector Store RAG.json` direpresentasikan sebagai pipeline RAG dengan komponen utama:

- `Knowledge`: dokumen HRD di-ingest dan di-retrieve
- `EmbeddingModel`: provider embedding Gemini
- `Agent`: model generatif untuk menghasilkan jawaban
- `Prompt Template`: format prompt final beserta konteks
- `Parser`: ekstraksi teks dari hasil retrieval
- `Chat Output`: hasil jawaban untuk diberikan ke frontend

## 4. Schema Data Dokumen

Dokumen HRD di folder `hrd-docs/` adalah sumber data untuk ingest ke vector store.

Tipe dokumen:

- markdown (`.md`)
- teks kebijakan HRD, SOP, FAQ, dan prompt agent

Tujuan:

- ingest konten text
- embedding konten ke vector store
- retrieval dokumen terkait pertanyaan pengguna

## 5. Schema Local Chroma Tool

File `chroma_tool.py` berisi utilitas lokal untuk ingest/query dengan Chroma.
Package yang dipakai:

- `chromadb`
- `sentence-transformers`

Schema penggunaan:

- `python chroma_tool.py ingest --docs hrd-docs`
- `python chroma_tool.py query "<pertanyaan>"`

Data output:

- indeks Chroma lokal
- query text + metadata

## 6. Schema UI

`streamlit_app.py` saat ini memiliki struktur UI berikut:

- Header card
- Sidebar info + contoh pertanyaan + tombol reset
- Chat area dengan:
  - welcome message bila chat kosong
  - message bubble untuk user
  - message bubble untuk assistant
  - `st.chat_input` sebagai input

Style kustom menggunakan CSS inline di Streamlit:

- `.chat-bubble`
- `.user-bubble`
- `.assistant-bubble`
- `.sidebar-card`
- `.header-card`

## 7. Schema Deployment

### 7.1 Cloud Run

Deploy ke Google Cloud Run menggunakan service `langflow`.

### 7.2 Secrets / env vars

- Frontend: `LANGFLOW_URL`, `FLOW_ID`, `LANGFLOW_API_KEY`
- Backend: `GEMINI_API_KEY`

### 7.3 Persistence

Saat ini persistence vector store di Cloud Run belum diverifikasi.
Untuk produksi, schema persistence yang direkomendasikan meliputi:

- backend vector DB terpisah
- Chroma server / DuckDB+Parquet dengan storage eksternal
- GCS / penyimpanan persistent lainnya

## 8. Catatan Tambahan

- `api_key` yang disebutkan di metadata flow bisa saja masih muncul sebagai `google_api_key`, tetapi implementasi runtime sekarang menggunakan `GEMINI_API_KEY`.
- `LANGFLOW_API_KEY` berbeda dengan `GEMINI_API_KEY`.
- `schema.md` ini dibuat untuk membantu memahami kondisi saat ini dan mempermudah maintenance / integrasi berikutnya.
