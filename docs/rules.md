# Rules for Langflow-Bob Project

Dokumen ini menjelaskan aturan penggunaan, konfigurasi, dan batasan penting untuk project `langflow-bob` berdasarkan kondisi saat ini.

## 1. Aturan Umum

- Gunakan branch `main` hanya untuk perubahan yang sudah teruji dan siap dipublish.
- Semua perubahan besar (desain UI, arsitektur, persistence, integrasi MCP) harus didokumentasikan di `README.md`, `ARCHITECTURE.md`, atau `PERSISTENCE_PLAN.md`.
- File baru yang dibuat untuk deskripsi arsitektur atau schema harus ditambahkan ke repository dan dirujuk dari `README.md`.

## 2. Konfigurasi Environment

### 2.1 Streamlit App

- `LANGFLOW_URL` harus menunjuk ke endpoint Langflow yang valid.
- `FLOW_ID` harus diisi dengan ID flow Langflow yang benar.
- `LANGFLOW_API_KEY` harus digunakan hanya untuk request ke Langflow API.
- Format request harus:
  - Method: `POST`
  - Endpoint: `{LANGFLOW_URL}/api/v1/run/{FLOW_ID}?stream=false`
  - Headers: `Content-Type: application/json`, `x-api-key: {LANGFLOW_API_KEY}`

### 2.2 Langflow Cloud Run

- `GEMINI_API_KEY` harus tersedia sebagai environment variable di Cloud Run.
- Jangan campur `LANGFLOW_API_KEY` dengan `GEMINI_API_KEY`.
- `GEMINI_API_KEY` hanya untuk provider embedding/model, sementara `LANGFLOW_API_KEY` untuk otentikasi HTTP ke Langflow.

## 3. Aturan UI dan UX

- `streamlit_app.py` harus menjaga session state pengguna agar percakapan tetap berlanjut selama sesi.
- Tampilkan pesan fallback yang jelas jika koneksi ke Langflow gagal atau timeout.
- Sidebar harus berisi informasi singkat, contoh pertanyaan, dan tombol reset riwayat chat.
- Setiap perubahan UI besar harus juga diperbarui di `design.md`.

## 4. Aturan Data & Vector Store

- Dokumen HRD hanya boleh berasal dari folder `hrd-docs/`.
- Jangan letakkan dokumen HRD sensitif di repo publik tanpa enkripsi atau kontrol akses.
- Vector store lokal harus hanya digunakan untuk development/testing.
- Untuk produksi, gunakan persistence eksternal atau backend vector DB terpisah.
- `PERSISTENCE_PLAN.md` harus menjadi acuan jika ingin mengubah arsitektur persistence.

## 5. Aturan Deploy & Operasi

- Pastikan `Cloud Run` memiliki konfigurasi yang sama dengan `Langflow` endpoint dan env vars.
- Jika men-deploy ulang, verifikasi kembali `LANGFLOW_URL`, `FLOW_ID`, dan `GEMINI_API_KEY`.
- Gunakan `check_env.py` atau file serupa untuk memvalidasi environment jika tersedia.

## 6. Aturan Dokumentasi

- Tambahkan file dokumentasi baru jika menambahkan komponen penting baru seperti:
  - `schema.md`
  - `ERD.md`
  - `ARCHITECTURE.md`
  - `PERSISTENCE_PLAN.md`
- Referensikan dokumen baru tersebut dari `README.md`.
- Update dokumentasi bila ada perubahan pada:
  - flow Langflow
  - env vars
  - stack teknologi
  - arsitektur deployment

## 7. Batasan yang Diketahui

- Cloud Run tidak memberikan persistence file sistem lokal tanpa konfigurasi tambahan.
- `streamlit_app.py` saat ini mengandalkan respons API Langflow dengan struktur JSON tertentu.
- Jika flow Langflow berubah, update parsing di `streamlit_app.py`.
- Pastikan `langflow/Vector Store RAG.json` tetap sinkron dengan flow yang dijalankan di produksi.

## 8. Best Practices

- Jangan commit secret atau API key ke repository.
- Gunakan secrets manager di Cloud Run atau Streamlit untuk konfigurasi sensitif.
- Uji dulu setiap integrasi baru secara lokal sebelum push ke remote.
- Simpan catatan perubahan besar di commit message yang jelas.
