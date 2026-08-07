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
│   └── Vector Store RAG.json   # Flow Langflow (siap import)
├── .bob/
│   └── mcp.json                # Konfigurasi MCP untuk IBM Bob
└── README.md
```

---

## 🏗️ Arsitektur

```
User
 │
 ▼
IBM Bob (MCP Client)
 │  uvx mcp-proxy (stdio → streamable HTTP)
 ▼
Langflow MCP Endpoint
(localhost:7862)
 │
 ▼
Vector Store RAG Flow
 ├── Knowledge (Ingest / Retrieve)
 ├── Embedding Model (gemini-embedding-2, 3072 dimensi)
 ├── Agent (gemini-3.5-flash-lite)
 ├── Prompt Template
 ├── Parser
 └── Chat Output
```

---

## ⚙️ Stack Teknologi

| Komponen | Detail |
|----------|--------|
| **Langflow** | v1.11.2 — platform visual untuk pipeline AI |
| **LLM Agent** | Google Gemini 3.5 Flash Lite |
| **Embedding Model** | `gemini-embedding-2` (Google Generative AI) |
| **Dimensi Embedding** | **3072** (`output_dimensionality`) |
| **Vector Store** | Langflow Knowledge component |
| **MCP Transport** | Streamable HTTP via `mcp-proxy` |
| **MCP Client** | IBM Bob |

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
     gemini-3.5-flash-lite
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
uvx mcp-proxy
  │  streamable HTTP
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

- [Langflow](https://langflow.org) berjalan di `localhost:7862`
- [IBM Bob](https://www.ibm.com/products/bob) terinstall
- [uv / uvx](https://docs.astral.sh/uv/getting-started/installation/) terinstall

```bash
# Cek uvx tersedia
uvx --version
```

### 1. Import Flow ke Langflow

1. Buka Langflow di `http://localhost:7862`
2. Klik **Import** di halaman Projects
3. Upload file `langflow/Vector Store RAG.json`
4. Pastikan field **Dimensions** di komponen **Embedding Model** bernilai `3072`

### 2. Setup API Key Google

1. Di Langflow, buka **Settings → Global Variables**
2. Tambahkan Google API Key untuk komponen **Agent** dan **Embedding Model**
3. Atau isi langsung di field **API Key** masing-masing komponen

### 3. Aktifkan MCP di IBM Bob

File `.bob/mcp.json` sudah tersedia di repo ini. Bob akan otomatis membaca config ini jika workspace dibuka di folder repo.

```json
{
  "mcpServers": {
    "lf-starter_project": {
      "command": "uvx",
      "args": [
        "mcp-proxy",
        "--transport",
        "streamablehttp",
        "http://localhost:7862/api/v1/mcp/project/05688c3b-4f2e-4b3e-995d-933594bd00c3/streamable"
      ]
    }
  }
}
```

> ⚠️ **Catatan:** `project_id` di URL (`05688c3b-...`) adalah ID project spesifik di instalasi Langflow lokal. Sesuaikan jika menggunakan instalasi berbeda.

### 4. Ingest Dokumen

1. Buka flow di Langflow
2. Set komponen **Knowledge** ke mode **Ingest**
3. Upload atau masukkan dokumen yang ingin di-index
4. Jalankan flow untuk menyimpan embedding ke vector store

### 5. Test via Bob

Setelah semua berjalan, Bob akan memiliki tool `vector_store_rag`. Coba tanya di Bob:

> *"Cari informasi tentang [topik dari dokumen kamu]"*

---

## ⚠️ Catatan Penting

- **Konsistensi dimensi:** Pastikan dimensi embedding **selalu 3072** baik saat Ingest maupun Retrieve. Jika sudah ada data lama dengan dimensi berbeda, hapus vector store dan ingest ulang.
- **Auto-login:** Langflow berjalan dalam mode `LANGFLOW_AUTO_LOGIN` — tidak perlu API key untuk akses dari localhost.
- **Secrets:** Jangan commit API key ke repo. Semua field `api_key` di flow dibiarkan kosong dan diisi melalui Global Variables Langflow.

---

## 📄 Lisensi

MIT
