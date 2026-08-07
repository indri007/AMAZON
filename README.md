# langflow-bob

Integrasi **Langflow Vector Store RAG** dengan **IBM Bob** menggunakan MCP (Model Context Protocol).

---

## 📌 Deskripsi Project

Project ini menghubungkan IBM Bob (AI coding assistant) dengan Langflow sebagai backend RAG (*Retrieval-Augmented Generation*). Langflow mengelola pipeline pencarian dokumen berbasis vector store, sementara Bob mengakses pipeline tersebut sebagai tool melalui protokol MCP.

**Use case utama:** tanya-jawab berbasis dokumen — upload dokumen → disimpan sebagai vektor embedding → Bob bisa retrieve dan menjawab pertanyaan berdasarkan isi dokumen tersebut.

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
└── README.md
```

---

## 🏗️ Arsitektur

```
User
 │
 ▼
IBM Bob (MCP Client)
 │  uvx mcp-proxy@0.9.0 (stdio → streamable HTTP)
 │  x-api-key: <langflow-api-key>
 ▼
Langflow MCP Endpoint
(localhost:7862)
 │
 ▼
Vector Store RAG Flow
 ├── Knowledge (Ingest / Retrieve)
 ├── Embedding Model (gemini-embedding-2, 3072 dimensi)
 ├── Agent (gemini-2.0-flash-lite)
 ├── Prompt Template
 ├── Parser
 └── Chat Output
```

---

## ⚙️ Stack Teknologi

| Komponen | Detail |
|----------|--------|
| **Langflow** | v1.11.2 — platform visual untuk pipeline AI |
| **LLM Agent** | Google Gemini 2.0 Flash Lite |
| **Embedding Model** | `gemini-embedding-2` (Google Generative AI) |
| **Dimensi Embedding** | **3072** (`output_dimensionality`) |
| **Vector Store** | Langflow Knowledge component |
| **MCP Proxy** | `mcp-proxy@0.9.0` via `uvx` |
| **MCP Transport** | Streamable HTTP |
| **MCP Client** | IBM Bob |
| **Port** | `7862` |

---

## 🔄 PRD Workflow Langflow

### 1. Fase Ingest (Simpan Dokumen)

```
Dokumen/Teks
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
Vector Store (tersimpan)
```

**Tujuan:** Mengubah dokumen menjadi vektor embedding 3072 dimensi dan menyimpannya ke vector store internal Langflow.

---

### 2. Fase Retrieve + Generate (Tanya Jawab)

```
User Question (Chat Input)
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
   assistant..." + context + question
               │
               ▼
           [Agent]
    gemini-2.0-flash-lite
    + MCP Tools (vector_store_rag)
               │
               ▼
         [Chat Output]
```

**Tujuan:** Menerima pertanyaan, mencari dokumen relevan di vector store, menyusun prompt dengan konteks, lalu menghasilkan jawaban via LLM.

---

### 3. Akses via MCP (IBM Bob)

```
IBM Bob
  │  stdio
  ▼
uvx mcp-proxy@0.9.0
  │  streamable HTTP + x-api-key
  ▼
Langflow MCP Endpoint
/api/v1/mcp/project/{project_id}/streamable
  │
  ▼
Tool: vector_store_rag
(menjalankan flow Retrieve + Generate)
```

**Tujuan:** Bob dapat memanggil flow RAG sebagai tool MCP, sehingga bisa menjawab pertanyaan berbasis dokumen langsung dari dalam chat Bob.

---

## 🚀 Setup & Instalasi

### Prasyarat

- [Langflow](https://langflow.org) v1.11.2 berjalan di `localhost:7862`
- [IBM Bob](https://www.ibm.com/products/bob) terinstall
- [uv / uvx](https://docs.astral.sh/uv/getting-started/installation/) v0.11+ terinstall
- Google API Key (Gemini)

```bash
# Cek uvx tersedia
uvx --version

# Pastikan mcp-proxy versi 0.9.0 bisa jalan
uvx mcp-proxy@0.9.0 --version
```

### 1. Import Flow ke Langflow

1. Buka Langflow di `http://localhost:7862`
2. Klik **Import** di halaman Projects
3. Upload file `langflow/Vector Store RAG.json`
4. Pastikan field **Dimensions** di komponen **Embedding Model** bernilai `3072`

### 2. Setup API Key Google (Gemini)

1. Buat API key di [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Di Langflow, buka **Settings → Global Variables**
3. Tambahkan variable `GOOGLE_API_KEY` dengan value API key kamu
4. Komponen **Agent** dan **Embedding Model** akan otomatis menggunakan variable ini

> ⚠️ **Jangan** simpan API key langsung di file flow atau commit ke git.

### 3. Buat Langflow API Key

Langflow v1.5+ memerlukan API key untuk akses endpoint MCP:

1. Buka `http://localhost:7862`
2. Klik **ikon profil** (kanan atas) → **Settings → API Keys**
3. Klik **+ Add New** → beri nama (misal: `bob-mcp`)
4. Copy API key yang muncul (format: `sk-xxxx...`)

### 4. Aktifkan MCP di IBM Bob

File `.bob/mcp.json` sudah tersedia di repo ini dengan konfigurasi:

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

> ⚠️ Ganti `<LANGFLOW_API_KEY>` dengan API key Langflow dari langkah sebelumnya.  
> ⚠️ `project_id` (`05688c3b-...`) adalah ID project spesifik. Sesuaikan jika menggunakan instalasi Langflow yang berbeda.

### 5. Ingest Dokumen

1. Buka flow **Vector Store RAG** di Langflow
2. Set komponen **Knowledge** ke mode **Ingest**
3. Upload atau masukkan dokumen yang ingin di-index
4. Jalankan flow untuk menyimpan embedding ke vector store

### 6. Test via Bob

Setelah semua berjalan, Bob akan memiliki tool `vector_store_rag`. Coba tanya di Bob:

> *"Cari informasi tentang [topik dari dokumen kamu]"*

---

## 🩺 Troubleshooting

### Error: `cannot import name 'request_ctx'`
Versi `mcp-proxy` terbaru tidak kompatibel dengan `mcp` SDK terbaru.  
**Solusi:** Gunakan `mcp-proxy@0.9.0` (sudah dikonfigurasi di `.bob/mcp.json`).

### Error: `401 Unauthorized` / `No authentication credentials provided`
Langflow v1.5+ memerlukan API key.  
**Solusi:** Pastikan `--header x-api-key:<key>` sudah ada di config MCP.

### Error: `404 Not Found` pada endpoint A2A
Flow belum di-enable sebagai A2A agent.  
**Solusi:** Buka flow di Langflow → Settings → aktifkan **"Enable A2A"**.

### MCP tidak terhubung setelah update config
**Solusi:** Reload window Bob: `Cmd+Shift+P` → **Reload Window**.

---

## ⚠️ Catatan Penting

- **Konsistensi dimensi:** Pastikan dimensi embedding **selalu 3072** baik saat Ingest maupun Retrieve. Jika sudah ada data lama dengan dimensi berbeda, hapus vector store dan ingest ulang.
- **mcp-proxy versi:** Gunakan `mcp-proxy@0.9.0` — versi lebih baru saat ini tidak kompatibel.
- **Secrets:** Jangan commit API key (Langflow maupun Google) ke repo.
- **Port:** Langflow berjalan di port `7862` (bukan default `7860`).

---

## 📄 Lisensi

MIT
