# langflow-bob

Integrasi **Langflow Vector Store RAG** dengan **IBM Bob** menggunakan MCP (Model Context Protocol) — dideploy di **Google Cloud Run** dan diakses via **Streamlit Cloud**.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://indri007-langflow-bob.streamlit.app)

---

## 📌 Deskripsi Project

Project ini menghubungkan IBM Bob (AI coding assistant) dengan Langflow sebagai backend RAG (*Retrieval-Augmented Generation*). Langflow mengelola pipeline pencarian dokumen berbasis vector store, sementara Bob mengakses pipeline tersebut sebagai tool melalui protokol MCP.

**Use case utama:** Chatbot HRD Virtual — dokumen kebijakan HRD di-ingest ke vector store → user bisa tanya-jawab seputar HRD melalui Streamlit app atau IBM Bob.

---

## 🔗 Live Links

| Layanan | URL |
|---------|-----|
| **Streamlit App (HRD Chatbot)** | https://indri007-langflow-bob.streamlit.app |
| **Langflow Cloud Run** | https://langflow-192433070716.asia-southeast2.run.app |
| **GitHub Repo** | https://github.com/indri007/langflow-bob |


---

## 🗂️ Struktur Repository

```
langflow-bob/
├── langflow/
│   └── Vector Store RAG.json       # Flow Langflow (siap import)
├── hrd-docs/
│   ├── faq_hrd.md                  # FAQ HRD knowledge base
│   ├── Dokumentasi_Scope_*.md      # Scope & batasan pengujian chatbot
│   └── prompts/
│       ├── agent1_router.md
│       ├── agent2_query_reformulation.md
│       ├── agent3_retrieval_grounding.md
│       ├── agent4_cs_responder.md
│       ├── agent5_hrd_interviewer.md
│       └── agent6_evaluator.md
├── .bob/
│   └── mcp.json                    # Konfigurasi MCP untuk IBM Bob
├── streamlit_app.py                # Streamlit HRD Chatbot app
└── README.md
```

---

## 🏗️ Arsitektur

```
User (Browser)
     │
     ▼
Streamlit Cloud App
(indri007-langflow-bob.streamlit.app)
     │  HTTP POST /api/v1/run/{flow_id}
     │  x-api-key: sk-xxx
     ▼
Langflow — Google Cloud Run
(langflow-192433070716.asia-southeast2.run.app)
     │
     ▼
Vector Store RAG Flow
 ├── Knowledge (Ingest / Retrieve)
 ├── Embedding Model (gemini-embedding-2, 3072 dim)
 ├── Agent (gemini-2.0-flash-lite)
 ├── Prompt Template
 ├── Parser
 └── Chat Output

──────────── ATAU via IBM Bob ────────────

IBM Bob (MCP Client)
     │  uvx mcp-proxy@0.9.0
     │  streamable HTTP + x-api-key
     ▼
Langflow MCP Endpoint
/api/v1/mcp/project/{project_id}/streamable
     │
     ▼
Tool: vector_store_rag
```

---

## ⚙️ Stack Teknologi

| Komponen | Detail |
|----------|--------|
| **Langflow** | v1.11.2 |
| **Deploy** | Google Cloud Run (`asia-southeast2`) |
| **LLM Agent** | Google Gemini 2.0 Flash Lite |
| **Embedding Model** | `gemini-embedding-2` (3072 dimensi) |
| **Vector Store** | Langflow Knowledge component |
| **Frontend** | Streamlit (Streamlit Cloud) |
| **MCP Proxy** | `mcp-proxy@0.9.0` via `uvx` |
| **MCP Transport** | Streamable HTTP |
| **MCP Client** | IBM Bob |

---

## 🔄 PRD Workflow

### 1. Fase Ingest (Simpan Dokumen HRD)

```
Dokumen HRD (FAQ, SOP, Kebijakan)
     │
     ▼
[Knowledge — mode: Ingest]
     │
     ▼
[EmbeddingModel]
gemini-embedding-2
output_dimensionality: 3072
     │
     ▼
Vector Store (tersimpan di Langflow Cloud Run)
```

**Tujuan:** Mengubah dokumen HRD menjadi vektor embedding 3072 dimensi dan menyimpannya ke vector store Langflow Cloud Run.

---

### 2. Fase Retrieve + Generate (Tanya Jawab HRD)

```
User Question (Streamlit / IBM Bob)
     │
     ├──────────────────────────┐
     ▼                          ▼
[Knowledge — mode: Retrieve]  [Prompt Template]
     │  context (hasil search)  │
     └──────────┬───────────────┘
               ▼
          [Parser]
    (ekstrak teks dari JSON)
               │
               ▼
          [Prompt]
  "You are a retrieval-augmented
   HRD assistant..." + context + question
               │
               ▼
           [Agent]
    gemini-2.0-flash-lite
               │
               ▼
         [Chat Output]
```

---

### 3. Akses via Streamlit Cloud

```
User → Streamlit Cloud App
          │  POST /api/v1/run/{flow_id}
          │  x-api-key: sk-Jly1LDqkcEj-...
          ▼
     Langflow Cloud Run
     langflow-192433070716.asia-southeast2.run.app
```

### 4. Akses via IBM Bob (MCP)

```
IBM Bob → uvx mcp-proxy@0.9.0
          │  streamable HTTP
          │  x-api-key: sk-DlkWQSf...
          ▼
     Langflow MCP Endpoint (lokal)
     localhost:7862/api/v1/mcp/project/05688c3b.../streamable

     — ATAU —

     Langflow MCP Endpoint (Cloud Run)
     langflow-192433070716.asia-southeast2.run.app
     /api/v1/mcp/project/a2a1a234.../streamable
```

---

## 🚀 Setup & Instalasi

### Prasyarat

- [IBM Bob](https://www.ibm.com/products/bob) terinstall
- [uv / uvx](https://docs.astral.sh/uv/getting-started/installation/) v0.11+
- Google API Key dari [Google AI Studio](https://aistudio.google.com/app/apikey)

```bash
uvx --version          # cek uvx
uvx mcp-proxy@0.9.0 --version  # pastikan mcp-proxy 0.9.0 bisa jalan
```

---

### Opsi A: Pakai Langflow Cloud Run (Recommended)

Langflow sudah berjalan di Cloud Run — tidak perlu install lokal.

**1. Set Global Variable di Langflow Cloud Run**

Buka https://langflow-192433070716.asia-southeast2.run.app → **Settings → Global Variables** → tambah:
- Name: `GOOGLE_API_KEY`
- Value: API key dari Google AI Studio

**2. Aktifkan MCP di IBM Bob**

Edit `.bob/mcp.json`:

```json
{
  "mcpServers": {
    "lf-cloudrun": {
      "command": "uvx",
      "args": [
        "mcp-proxy@0.9.0",
        "--transport",
        "streamablehttp",
        "--header",
        "x-api-key:<LANGFLOW_API_KEY_CLOUD_RUN>",
        "https://langflow-192433070716.asia-southeast2.run.app/api/v1/mcp/project/a2a1a234-0b47-4007-a4e7-1d8fec7b3ebf/streamable"
      ]
    }
  }
}
```

**3. Ingest Dokumen HRD**

Buka https://langflow-192433070716.asia-southeast2.run.app → flow **Vector Store RAG** → Knowledge → mode **Ingest** → upload dokumen dari folder `hrd-docs/`.

---

### Opsi B: Jalankan Langflow Lokal

**1. Install & jalankan Langflow**

```bash
pip install langflow
langflow run --port 7862
```

**2. Import flow**

Buka `http://localhost:7862` → Import → upload `langflow/Vector Store RAG.json`

**3. Set API Key Google**

Langflow → **Settings → Global Variables** → tambah `GOOGLE_API_KEY`

**4. Buat Langflow API Key**

Langflow → **profil → Settings → API Keys → + Add New** → copy key (`sk-xxxx...`)

**5. Aktifkan MCP di IBM Bob**

```json
{
  "mcpServers": {
    "lf-vector-store-rag": {
      "command": "uvx",
      "args": [
        "mcp-proxy@0.9.0",
        "--transport",
        "streamablehttp",
        "--header",
        "x-api-key:<LANGFLOW_API_KEY>",
        "http://localhost:7862/api/v1/mcp/project/05688c3b-4f2e-4b3e-995d-933594bd00c3/streamable"
      ]
    }
  }
}
```

---

### Deploy Streamlit App

**1. Fork/clone repo ini ke GitHub**

**2. Buka [share.streamlit.io](https://share.streamlit.io) → New App → pilih repo ini**

**3. Set Secrets** (Settings → Secrets):

```toml
LANGFLOW_URL = "https://langflow-192433070716.asia-southeast2.run.app"
FLOW_ID = "d8eedd75-92a7-47f0-974a-b74c0062ea23"
LANGFLOW_API_KEY = "<LANGFLOW_API_KEY_CLOUD_RUN>"
```

---

## 🩺 Troubleshooting

### Error: `cannot import name 'request_ctx'`
Versi `mcp-proxy` terbaru tidak kompatibel.
**Solusi:** Gunakan `mcp-proxy@0.9.0`.

### Error: `401 Unauthorized`
Langflow v1.5+ wajib API key.
**Solusi:** Pastikan `--header x-api-key:<key>` ada di config MCP.

### Error: `❌ Tidak dapat terhubung ke Langflow`
Langflow tidak bisa diakses dari Streamlit Cloud jika pakai `localhost`.
**Solusi:** Gunakan URL Cloud Run sebagai `LANGFLOW_URL`.

### MCP tidak terhubung setelah update config
**Solusi:** Reload Bob: `Cmd+Shift+P` → **Reload Window**.

### Cold start Cloud Run lambat
**Solusi:** Set minimum instances = 1 di Cloud Run console.

---

## ⚠️ Catatan Penting

- **Dimensi embedding:** Selalu **3072** baik Ingest maupun Retrieve. Jika beda, hapus vector store dan ingest ulang.
- **mcp-proxy:** Gunakan `mcp-proxy@0.9.0` — versi lebih baru tidak kompatibel saat ini.
- **Secrets:** Jangan commit API key ke repo (Langflow maupun Google).
- **Cloud Run cold start:** Langflow bisa lambat ~30 detik setelah idle. Set min-instances=1 untuk produksi.

---

## 📄 Lisensi

MIT
