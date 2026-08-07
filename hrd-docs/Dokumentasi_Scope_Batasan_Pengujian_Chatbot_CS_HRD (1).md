# Dokumentasi Proyek: Sistem Chatbot CS & HRD Mockup Interview
## Berbasis Qdrant, Aiven, n8n, ANN, Gemini Embedding-001, dan Streamlit

**Versi:** 1.0
**Tanggal:** 23 Juli 2026

---

## 1. Latar Belakang dan Tujuan Proyek

Proyek ini bertujuan membangun sebuah sistem chatbot berbasis Retrieval-Augmented Generation (RAG) yang melayani dua fungsi utama: (1) chatbot Customer Service (CS) untuk menjawab pertanyaan pengguna secara otomatis, dan (2) chatbot HRD yang berfungsi sebagai mockup interview, yaitu simulasi wawancara kerja yang dapat digunakan kandidat untuk berlatih sebelum wawancara sesungguhnya.

Sistem dibangun dengan kombinasi teknologi berikut:

- **Qdrant** sebagai vector database untuk menyimpan dan mencari embedding dokumen menggunakan pendekatan ANN (Approximate Nearest Neighbor).
- **Aiven** sebagai penyedia database terkelola (managed database), digunakan untuk menyimpan data relasional seperti histori percakapan, log pengguna, dan metadata sesi.
- **n8n** sebagai orkestrator alur kerja (workflow automation) yang menghubungkan seluruh komponen: input pengguna, pemanggilan embedding, pencarian vektor, pemanggilan LLM, dan penulisan log ke database.
- **Gemini Embedding-001** sebagai model embedding untuk mengubah teks menjadi representasi vektor yang akan disimpan dan dicari di Qdrand.
- **ANN (Approximate Nearest Neighbor)** sebagai metode pencarian kemiripan vektor yang efisien di dalam Qdrant, dibandingkan pencarian exact k-NN yang mahal secara komputasi.
- **Streamlit** sebagai antarmuka pengguna (front-end), dengan autentikasi login menggunakan Google OAuth.

Dokumen ini disusun untuk memberikan kejelasan mengenai apa saja yang termasuk dalam ruang lingkup (in-scope), apa yang secara eksplisit berada di luar ruang lingkup (out-of-scope), batasan teknis dan operasional sistem, serta metodologi dan alat pengujian yang akan digunakan untuk memvalidasi bahwa sistem berjalan sesuai spesifikasi.

---

## 2. Ruang Lingkup (In-Scope)

### 2.1 Autentikasi dan Manajemen Pengguna
- Login pengguna menggunakan Google OAuth 2.0 yang terintegrasi di aplikasi Streamlit.
- Penyimpanan profil dasar pengguna (nama, email, foto profil dari akun Google) ke database Aiven setelah login berhasil.
- Manajemen sesi login (session state) di sisi Streamlit, termasuk logout dan refresh token bila diperlukan.

### 2.2 Modul Chatbot Customer Service (CS)
- Penerimaan pertanyaan pengguna dalam bahasa Indonesia dan/atau Inggris melalui antarmuka chat Streamlit.
- Proses embedding pertanyaan pengguna menggunakan Gemini Embedding-001.
- Pencarian dokumen relevan (FAQ, knowledge base, dokumen kebijakan) di Qdrant menggunakan pendekatan ANN.
- Penyusunan jawaban berbasis konteks yang diambil (retrieval) untuk kemudian diteruskan ke model bahasa (LLM) guna menghasilkan jawaban akhir.
- Pencatatan setiap percakapan (pertanyaan, jawaban, dokumen yang dirujuk, timestamp) ke database Aiven untuk keperluan audit dan evaluasi.

### 2.3 Modul Chatbot HRD Mockup Interview
- Simulasi wawancara kerja berbasis teks, dengan chatbot berperan sebagai pewawancara (interviewer).
- Bank pertanyaan wawancara yang disimpan dan diambil melalui pencarian embedding di Qdrant, disesuaikan dengan posisi/peran yang dipilih pengguna.
- Alur wawancara bertahap (multi-turn) yang dikelola melalui workflow n8n, termasuk logika percabangan pertanyaan lanjutan berdasarkan jawaban pengguna sebelumnya.
- Pemberian umpan balik (feedback) sederhana di akhir sesi wawancara berdasarkan pola jawaban pengguna (misalnya kelengkapan jawaban, penggunaan kata kunci relevan).
- Penyimpanan transkrip lengkap sesi wawancara ke database Aiven, terhubung dengan akun pengguna yang login.

### 2.4 Orkestrasi Alur Kerja dengan n8n
- Workflow n8n sebagai penghubung antara Streamlit (front-end), Gemini Embedding-001 (embedding), Qdrant (vector search), LLM (generasi jawaban), dan Aiven (penyimpanan data).
- Webhook n8n sebagai endpoint yang dipanggil oleh Streamlit untuk memproses setiap pesan pengguna.
- Node-node n8n yang menangani: validasi input, pemanggilan API embedding, query ke Qdrant, pemanggilan LLM, penulisan log ke Aiven, dan pengembalian respons ke Streamlit.
- Error handling dasar di level workflow (retry otomatis untuk kegagalan pemanggilan API, notifikasi kegagalan ke log).

### 2.5 Vector Database dan Pencarian ANN
- Pembuatan dan pengelolaan koleksi (collection) di Qdrant untuk dua domain terpisah: knowledge base CS dan bank pertanyaan HRD.
- Konfigurasi parameter ANN (misalnya HNSW: `ef_construct`, `m`, `ef_search`) untuk menyeimbangkan kecepatan pencarian dan akurasi hasil.
- Proses indexing awal (bulk upload) dokumen CS dan bank soal HRD ke Qdrant.
- Mekanisme pembaruan (update/upsert) data di Qdrant ketika ada dokumen baru atau perubahan konten.

### 2.6 Antarmuka Pengguna (Streamlit)
- Halaman login dengan tombol "Login dengan Google".
- Halaman utama dengan pilihan antara chatbot CS dan mode mockup interview HRD.
- Tampilan riwayat percakapan per pengguna (diambil dari Aiven).
- Antarmuka chat interaktif standar (input teks, bubble chat, indikator sedang mengetik).

### 2.7 Dokumentasi dan Pengujian
- Dokumentasi arsitektur sistem, alur data, dan konfigurasi masing-masing komponen.
- Pengujian fungsional, integrasi, dan performa sebagaimana dijelaskan pada Bagian 4.

---

## 3. Di Luar Ruang Lingkup (Out-of-Scope)

Untuk menjaga fokus proyek dan mengelola ekspektasi, berikut adalah hal-hal yang **tidak** termasuk dalam ruang lingkup pengerjaan:

### 3.1 Aspek Model dan Kecerdasan Buatan
- Pelatihan ulang (fine-tuning atau training from scratch) model embedding maupun model bahasa besar (LLM). Sistem hanya menggunakan Gemini Embedding-001 dan LLM pihak ketiga melalui API, bukan model yang dilatih sendiri.
- Evaluasi akademis mendalam terhadap kualitas embedding (misalnya benchmark terhadap dataset standar seperti MTEB) tidak menjadi bagian dari proyek ini kecuali disebutkan secara terpisah.
- Deteksi emosi, analisis sentimen mendalam, atau penilaian psikometri terhadap jawaban kandidat pada sesi mockup interview HRD. Umpan balik yang diberikan bersifat sederhana dan berbasis pola/kata kunci, bukan penilaian psikologis profesional.
- Sistem tidak menggantikan proses rekrutmen HRD yang sesungguhnya; mockup interview murni bersifat latihan/simulasi bagi kandidat, bukan alat keputusan penerimaan kerja.

### 3.2 Infrastruktur dan Skalabilitas
- Penyediaan infrastruktur multi-region atau high-availability tingkat enterprise (load balancer aktif-aktif, disaster recovery lintas region) tidak termasuk dalam versi awal proyek.
- Optimasi biaya (cost optimization) mendalam terhadap penggunaan API Gemini, Qdrant Cloud, maupun Aiven berada di luar cakupan versi pertama, meskipun estimasi biaya dasar akan dicatat di dokumentasi.
- Containerization penuh dengan Kubernetes/orkestrasi container skala besar tidak menjadi bagian wajib; deployment cukup menggunakan layanan cloud sederhana (misalnya Streamlit Community Cloud, Cloud Run, atau VM tunggal).

### 3.3 Keamanan Lanjutan
- Audit keamanan tingkat lanjut (penetration testing formal, sertifikasi ISO 27001, atau kepatuhan SOC 2) tidak termasuk dalam proyek ini.
- Enkripsi end-to-end tingkat lanjut pada transkrip wawancara (di luar enkripsi standar in-transit/at-rest yang disediakan Aiven dan Qdrant Cloud) tidak dicakup.
- Deteksi dan pencegahan prompt injection tingkat lanjut hanya dilakukan pada level dasar (sanitasi input sederhana), bukan sistem keamanan LLM tingkat produksi enterprise.

### 3.4 Fitur Tambahan yang Tidak Termasuk
- Dukungan multi-bahasa di luar Bahasa Indonesia dan Inggris.
- Integrasi suara (voice-to-text atau text-to-speech) untuk sesi mockup interview; sistem murni berbasis teks.
- Integrasi dengan sistem ATS (Applicant Tracking System) pihak ketiga atau software HRIS perusahaan.
- Aplikasi mobile native (Android/iOS); antarmuka hanya berbasis web melalui Streamlit.
- Dashboard analitik lanjutan (business intelligence) untuk pihak manajemen; laporan yang tersedia hanya berupa data mentah/log dasar di Aiven.
- Notifikasi email atau push notification otomatis kepada pengguna.

### 3.5 Data dan Konten
- Pembuatan konten knowledge base CS dan bank soal HRD dari nol dianggap sebagai tanggung jawab tim/klien yang menyediakan materi; proyek ini hanya menyediakan mekanisme ingest dan pencarian, bukan penulisan konten substantif.
- Validasi kebenaran faktual dari jawaban LLM secara manual oleh tim ahli domain tidak termasuk dalam scope teknis, meskipun mekanisme logging disediakan untuk memungkinkan audit di kemudian hari.

---

## 4. Batasan Sistem (Constraints)

### 4.1 Batasan Teknis
1. **Ketergantungan pada layanan pihak ketiga**: Sistem sepenuhnya bergantung pada ketersediaan (uptime) Gemini API, Qdrant Cloud, Aiven, dan n8n (baik versi cloud maupun self-hosted). Gangguan pada salah satu layanan ini akan memengaruhi fungsi keseluruhan sistem.
2. **Batas kuota API**: Pemanggilan Gemini Embedding-001 dan LLM tunduk pada rate limit dan kuota yang ditetapkan oleh penyedia. Penggunaan intensif secara bersamaan oleh banyak pengguna dapat menyebabkan throttling atau penundaan respons.
3. **Latensi pipeline**: Karena alur permintaan melewati beberapa tahap (Streamlit → n8n webhook → Gemini Embedding → Qdrant ANN search → LLM → Aiven logging → respons kembali ke Streamlit), total latensi end-to-end berpotensi berada pada kisaran 2–6 detik tergantung beban dan jarak jaringan, dan ini merupakan batasan arsitektural yang melekat pada desain berbasis orkestrasi seperti ini.
4. **Akurasi ANN bukan exact search**: Karena Qdrant menggunakan pendekatan ANN (misalnya algoritma HNSW), hasil pencarian bersifat approximate, bukan exact nearest neighbor. Ada kemungkinan kecil dokumen yang sebenarnya paling relevan tidak selalu berada di urutan teratas hasil pencarian, terutama pada parameter `ef_search` yang rendah.
5. **Konsistensi data antar sistem**: Karena data tersebar di dua sistem berbeda (Qdrant untuk vektor, Aiven untuk data relasional), terdapat risiko inkonsistensi apabila salah satu proses gagal di tengah jalan (misalnya embedding berhasil disimpan di Qdrant namun log gagal ditulis ke Aiven). Mekanisme rollback penuh (distributed transaction) tidak diimplementasikan pada versi ini; hanya retry sederhana di level workflow n8n.
6. **Batasan konteks LLM**: Jumlah dokumen yang dapat disertakan sebagai konteks (context window) dalam satu permintaan ke LLM dibatasi oleh batas token model yang digunakan, sehingga jumlah dokumen hasil retrieval yang disertakan perlu dibatasi (biasanya top-k antara 3–5 dokumen).

### 4.2 Batasan Fungsional
1. Chatbot HRD mockup interview memberikan simulasi dan umpan balik dasar, bukan penilaian kelulusan resmi.
2. Jawaban chatbot CS terbatas pada cakupan dokumen yang telah di-index ke Qdrant; pertanyaan di luar knowledge base akan dijawab dengan indikasi "informasi tidak tersedia" alih-alih berhalusinasi, namun risiko halusinasi LLM tetap ada dan tidak bisa dihilangkan sepenuhnya (hanya diminimalkan lewat prompt grounding).
3. Login hanya mendukung akun Google; pengguna tanpa akun Google tidak dapat mengakses sistem pada versi ini.

### 4.3 Batasan Non-Fungsional
1. **Skalabilitas awal**: Sistem dirancang untuk skala kecil-menengah (uji coba/pilot), bukan untuk trafik produksi skala besar dengan ribuan pengguna simultan.
2. **Bahasa antarmuka**: UI Streamlit disusun dalam Bahasa Indonesia sebagai bahasa utama.
3. **Ketersediaan (availability)**: Target awal SLA bersifat best-effort, bukan komitmen uptime formal (misalnya 99.9%).

---

## 5. Arsitektur Alur Data (Ringkas)

Alur data pada sistem secara umum mengikuti tahapan berikut:

1. Pengguna login melalui Streamlit menggunakan Google OAuth → data profil disimpan/diperbarui di Aiven.
2. Pengguna mengetik pesan (pertanyaan CS atau jawaban wawancara HRD) di antarmuka Streamlit.
3. Streamlit mengirim payload ke webhook n8n.
4. Workflow n8n memanggil Gemini Embedding-001 untuk mengubah teks menjadi vektor.
5. Vektor dikirim ke Qdrant untuk pencarian ANN terhadap koleksi yang sesuai (knowledge base CS atau bank soal HRD).
6. Dokumen/konteks hasil pencarian dikembalikan ke n8n, kemudian disusun menjadi prompt untuk LLM.
7. LLM menghasilkan respons (jawaban CS atau pertanyaan/feedback wawancara HRD berikutnya).
8. n8n mencatat seluruh interaksi (input, hasil retrieval, output LLM, timestamp, user ID) ke database Aiven.
9. Respons akhir dikirim kembali ke Streamlit dan ditampilkan ke pengguna.

---

## 6. Alat dan Metodologi Pengujian

Pengujian sistem dibagi menjadi beberapa lapisan (layer), dari unit hingga end-to-end, agar setiap komponen dapat divalidasi secara independen maupun terintegrasi.

### 6.1 Pengujian Unit (Unit Testing)
- **Alat**: `pytest` (Python) untuk menguji fungsi-fungsi pemrosesan di sisi Streamlit dan skrip pendukung (misalnya fungsi formatting prompt, fungsi parsing respons API).
- **Cakupan pengujian**:
  - Fungsi pemanggilan Google OAuth (mock response token).
  - Fungsi format query sebelum dikirim ke embedding API.
  - Fungsi parsing hasil pencarian Qdrant menjadi struktur data yang siap digunakan di prompt LLM.

### 6.2 Pengujian Integrasi (Integration Testing)
- **Alat**: Postman atau Insomnia untuk menguji endpoint webhook n8n secara manual maupun otomatis melalui collection runner.
- **Cakupan pengujian**:
  - Uji koneksi n8n → Gemini Embedding API (memastikan payload dan response format sesuai kontrak API).
  - Uji koneksi n8n → Qdrant (memastikan query vektor berhasil dan mengembalikan hasil dengan skor kemiripan yang valid).
  - Uji koneksi n8n → Aiven (memastikan insert/update record berhasil dengan skema tabel yang benar).
  - Uji end-to-end workflow n8n menggunakan mode "Test Workflow" bawaan n8n, dengan data dummy pada setiap node.

### 6.3 Pengujian Fungsional Aplikasi (Functional Testing)
- **Alat**: Selenium atau Playwright untuk otomasi pengujian UI Streamlit (simulasi klik tombol login, pengisian form chat, verifikasi tampilan respons).
- **Cakupan pengujian**:
  - Skenario login Google OAuth berhasil dan gagal (misalnya token invalid, pengguna membatalkan login).
  - Skenario percakapan CS: pertanyaan yang ada di knowledge base vs pertanyaan di luar cakupan.
  - Skenario mockup interview HRD: alur pertanyaan bertahap, penyimpanan transkrip, dan tampilan feedback akhir.

### 6.4 Pengujian Vector Search dan Relevansi (Retrieval Evaluation)
- **Alat**: Skrip evaluasi kustom berbasis Python (menggunakan library seperti `numpy`/`pandas`) untuk menghitung metrik retrieval.
- **Metrik yang diukur**:
  - **Precision@k** dan **Recall@k**: mengukur seberapa relevan dokumen yang dikembalikan Qdrant pada top-k hasil pencarian terhadap ground truth yang telah disiapkan.
  - **Mean Reciprocal Rank (MRR)**: mengukur posisi rata-rata dokumen relevan pertama dalam hasil pencarian.
  - Perbandingan hasil ANN (Qdrant/HNSW) versus exact search sebagai baseline, untuk mengukur trade-off antara kecepatan dan akurasi pada berbagai konfigurasi parameter (`ef_search`, `m`).

### 6.5 Pengujian Performa dan Beban (Performance/Load Testing)
- **Alat**: `k6` atau `Locust` untuk simulasi banyak pengguna mengakses webhook n8n secara bersamaan.
- **Cakupan pengujian**:
  - Pengukuran latensi end-to-end pada beban rendah (1–5 pengguna simultan), sedang (10–20 pengguna), dan tinggi (50+ pengguna), untuk mengidentifikasi titik penurunan performa (bottleneck).
  - Pengukuran throughput maksimum n8n webhook sebelum terjadi antrian (queueing) atau timeout.
  - Monitoring resource usage (CPU, memori) pada instance n8n dan Streamlit selama uji beban.

### 6.6 Pengujian Keamanan Dasar (Basic Security Testing)
- **Alat**: OWASP ZAP (mode baseline scan) untuk pemindaian kerentanan dasar pada aplikasi web Streamlit.
- **Cakupan pengujian**:
  - Verifikasi bahwa endpoint webhook n8n tidak dapat diakses tanpa autentikasi/token yang sesuai.
  - Uji sanitasi input dasar untuk mencegah injeksi karakter berbahaya pada prompt (basic prompt injection check).
  - Verifikasi bahwa kredensial (API key Gemini, koneksi Aiven, koneksi Qdrant) tidak ter-hardcode di kode sumber maupun ter-expose di log aplikasi.

### 6.7 Pengujian Regresi (Regression Testing)
- **Alat**: GitHub Actions (CI pipeline) untuk menjalankan seluruh test suite (unit + integrasi) secara otomatis setiap kali ada perubahan kode yang di-push.
- **Tujuan**: memastikan perubahan pada satu komponen (misalnya update parameter ANN di Qdrant) tidak merusak fungsi lain yang sudah berjalan sebelumnya.

### 6.8 User Acceptance Testing (UAT)
- **Metode**: Sesi uji coba langsung bersama sejumlah pengguna perwakilan (misalnya tim internal atau kandidat uji coba untuk fitur mockup interview HRD).
- **Cakupan**: mengumpulkan umpan balik kualitatif mengenai relevansi jawaban chatbot CS, kualitas pengalaman simulasi wawancara HRD, dan kemudahan penggunaan antarmuka Streamlit secara keseluruhan.

---

## 7. Kriteria Keberhasilan (Acceptance Criteria)

Sebagai acuan bahwa sistem dianggap layak untuk tahap berikutnya (pilot/produksi terbatas), berikut kriteria minimal yang disarankan:

- Login Google OAuth berhasil pada lebih dari 95% percobaan pada kondisi jaringan normal.
- Latensi rata-rata end-to-end untuk satu putaran tanya-jawab tidak melebihi ambang batas yang disepakati (misalnya di bawah 6 detik pada beban normal).
- Precision@5 hasil pencarian Qdrant untuk knowledge base CS berada di atas ambang batas yang disepakati tim (misalnya minimal 0.7, disesuaikan dengan hasil uji awal).
- Seluruh transkrip sesi (baik CS maupun mockup interview HRD) tercatat lengkap di Aiven tanpa kehilangan data pada uji beban normal.
- Tidak ditemukan kredensial sensitif yang ter-expose pada hasil pemindaian keamanan dasar (OWASP ZAP baseline).

---

## 8. Panduan Prompt Engineering untuk 6 Agen

Di dalam pipeline n8n, sistem sebenarnya tidak hanya memanggil satu LLM sekali, melainkan menjalankan enam "agen" dengan peran dan prompt yang berbeda-beda, dipanggil secara berurutan atau kondisional dalam satu alur permintaan. Berikut adalah keenam agen tersebut beserta pendekatan prompt engineering yang disarankan untuk masing-masing.

### 8.1 Agen 1 — Router/Orkestrator (Intent Classifier)

**Peran**: Menentukan apakah pesan pengguna termasuk permintaan CS atau sesi mockup interview HRD, serta mendeteksi apakah pengguna ingin memulai, melanjutkan, atau mengakhiri sesi. Node ini biasanya berupa LLM call pertama di dalam workflow n8n sebelum masuk ke node percabangan (IF/Switch).

**Teknik yang disarankan**:
- **Role prompting** yang sangat sempit — agen ini hanya bertugas mengklasifikasi, bukan menjawab.
- **Output terstruktur (JSON)** agar mudah diparse oleh node n8n berikutnya, bukan output bebas.
- **Few-shot examples** untuk kasus ambigu (misalnya pesan "saya mau tanya soal interview besok" bisa disalahartikan sebagai CS padahal terkait HRD).
- **Negative instruction** eksplisit agar model tidak mencoba menjawab isi pertanyaan, hanya mengklasifikasi.

**Contoh system prompt**:
```
Anda adalah pengklasifikasi niat (intent classifier). Tugas Anda HANYA mengklasifikasikan
pesan pengguna ke salah satu kategori: "cs", "hrd_interview", atau "lainnya".
Jangan menjawab isi pertanyaan. Jangan menambahkan penjelasan.
Balas HANYA dalam format JSON: {"intent": "...", "confidence": 0.0-1.0}

Contoh:
Input: "Bagaimana cara reset password akun saya?"
Output: {"intent": "cs", "confidence": 0.95}

Input: "Saya mau latihan wawancara untuk posisi data analyst"
Output: {"intent": "hrd_interview", "confidence": 0.98}
```

### 8.2 Agen 2 — Query Reformulation (Penulis Ulang Kueri)

**Peran**: Menyempurnakan pertanyaan mentah pengguna menjadi kueri pencarian yang lebih optimal sebelum di-embed oleh Gemini Embedding-001 dan dicari di Qdrant. Penting terutama untuk percakapan multi-turn di mana pertanyaan lanjutan sering mengandung referensi implisit (misalnya "kalau yang tadi gimana?").

**Teknik yang disarankan**:
- **Chain-of-thought singkat** (bukan panjang) untuk menyelesaikan referensi implisit menggunakan histori percakapan sebelumnya.
- **Context injection**: sertakan 2–3 giliran percakapan terakhir sebagai konteks, bukan seluruh histori, untuk menghemat token dan mengurangi noise.
- **Pembatasan panjang output** — hasil akhir harus berupa satu kalimat kueri yang ringkas, bukan esai.

**Contoh system prompt**:
```
Anda menulis ulang pertanyaan pengguna menjadi kueri pencarian yang jelas dan mandiri
(self-contained), dengan menyelesaikan rujukan implisit dari histori percakapan.
Balas HANYA dengan satu kalimat kueri hasil tulisan ulang, tanpa tanda kutip,
tanpa penjelasan tambahan.

Histori:
User: Apa syarat pengajuan klaim asuransi?
Asisten: Syaratnya adalah KTP, polis aktif, dan bukti kejadian.
User: Kalau yang online gimana caranya?

Kueri hasil tulisan ulang: "Cara pengajuan klaim asuransi secara online"
```

### 8.3 Agen 3 — Retrieval Grounding (Penyusun Konteks)

**Peran**: Mengubah hasil mentah pencarian ANN dari Qdrant (potongan dokumen beserta skor kemiripan) menjadi konteks yang rapi dan siap disuntikkan ke prompt agen penjawab (Agen 4 atau Agen 5). Agen ini juga bertugas menyaring dokumen dengan skor kemiripan terlalu rendah agar tidak ikut menjadi konteks yang menyesatkan.

**Teknik yang disarankan**:
- **Thresholding eksplisit** dalam instruksi: dokumen dengan skor di bawah ambang batas tertentu diberi label "kurang relevan" atau dibuang.
- **Delimiter/tag XML** untuk memisahkan tiap sumber dokumen agar model penjawab bisa mengutip sumber dengan jelas dan tidak mencampur antar dokumen.
- **Instruksi ringkas, bukan generatif** — agen ini idealnya deterministik (bisa berupa skrip/kode biasa di n8n, bukan LLM call, kecuali diperlukan peringkasan otomatis).

**Contoh prompt (jika menggunakan LLM untuk meringkas konteks)**:
```
Susun ulang potongan dokumen berikut menjadi konteks yang ringkas dan terstruktur.
Beri label sumber pada setiap poin menggunakan tag <sumber id="...">...</sumber>.
Jangan menambahkan informasi yang tidak ada di dokumen. Jangan menjawab pertanyaan,
hanya menyusun konteks.
```

### 8.4 Agen 4 — CS Responder (Penjawab Customer Service)

**Peran**: Menghasilkan jawaban akhir untuk pengguna berdasarkan konteks yang telah disusun Agen 3. Ini adalah agen yang paling rawan berhalusinasi bila prompt-nya tidak dirancang dengan grounding yang ketat.

**Teknik yang disarankan**:
- **Grounding instruction tegas**: jawab hanya berdasarkan konteks yang diberikan; jika tidak ada di konteks, katakan tidak tersedia — jangan mengarang.
- **Positive & negative examples** untuk menunjukkan gaya jawaban yang diinginkan vs yang harus dihindari (misalnya jangan berjanji hal yang tidak ada di kebijakan).
- **Instruksi nada bicara** (tone) agar konsisten — misalnya sopan, ringkas, profesional, menggunakan Bahasa Indonesia baku namun ramah.
- **Batasan panjang jawaban** eksplisit agar tidak bertele-tele.

**Contoh system prompt**:
```
Anda adalah asisten Customer Service yang sopan dan ringkas. Jawab HANYA berdasarkan
<konteks> yang diberikan. Jika jawaban tidak ditemukan dalam konteks, katakan dengan
jujur: "Maaf, informasi tersebut belum tersedia, akan saya teruskan ke tim terkait."
Jangan mengarang kebijakan atau angka yang tidak tercantum di konteks.
Jawaban maksimal 4 kalimat.

<konteks>
{{hasil_dari_agen_3}}
</konteks>

Pertanyaan pengguna: {{pertanyaan}}
```

### 8.5 Agen 5 — HRD Interviewer (Pewawancara Simulasi)

**Peran**: Mengajukan pertanyaan wawancara secara bertahap, menyesuaikan pertanyaan lanjutan berdasarkan jawaban kandidat sebelumnya, dan menjaga alur wawancara tetap natural layaknya pewawancara sungguhan.

**Teknik yang disarankan**:
- **Persona/role prompting yang konsisten** — tentukan gaya pewawancara (formal, suportif, menantang) agar tidak berubah-ubah antar giliran.
- **State tracking via prompt**: sertakan ringkasan progres wawancara (posisi yang dilamar, jumlah pertanyaan yang sudah diajukan, topik yang sudah dibahas) di setiap pemanggilan, karena LLM tidak menyimpan memori sendiri di luar konteks yang dikirim.
- **Guardrail**: instruksikan agen untuk tidak memberikan jawaban "benar" kepada kandidat selama sesi berlangsung, hanya bertanya dan menggali lebih dalam.
- **Step-by-step reasoning tersembunyi** (opsional): minta model menentukan dulu topik pertanyaan berikutnya berdasarkan celah pada jawaban kandidat, baru menyusun kalimat pertanyaannya — namun keluarkan hanya pertanyaan akhirnya ke pengguna, bukan proses berpikirnya.

**Contoh system prompt**:
```
Anda berperan sebagai pewawancara HRD yang profesional namun suportif, sedang
mewawancarai kandidat untuk posisi: {{posisi}}.
Progres wawancara: sudah {{jumlah_pertanyaan}} pertanyaan diajukan, topik yang sudah
dibahas: {{daftar_topik}}.

Berdasarkan jawaban kandidat terakhir, ajukan SATU pertanyaan lanjutan yang relevan.
Jangan menilai benar/salah jawaban kandidat selama sesi berlangsung.
Jangan mengulang topik yang sudah dibahas kecuali untuk menggali lebih dalam.

Jawaban kandidat: {{jawaban_terakhir}}
```

### 8.6 Agen 6 — Evaluator/Feedback (Penilai Akhir Sesi)

**Peran**: Memberikan umpan balik ringkas di akhir sesi mockup interview, berdasarkan seluruh transkrip percakapan yang tersimpan di Aiven.

**Teknik yang disarankan**:
- **Rubrik eksplisit dalam prompt** (misalnya: kejelasan jawaban, penggunaan contoh konkret, relevansi dengan pertanyaan) agar penilaian konsisten antar sesi, bukan penilaian bebas yang subjektif.
- **Output terstruktur** (JSON atau poin-poin tetap) agar mudah ditampilkan di UI Streamlit maupun disimpan sebagai data terstruktur di Aiven.
- **Pembatasan nada**: instruksikan agar umpan balik bersifat konstruktif, bukan menghakimi, karena tujuan sistem adalah latihan, bukan penilaian kelulusan resmi (lihat batasan pada Bagian 3.1 dan 4.2).

**Contoh system prompt**:
```
Anda memberikan umpan balik konstruktif atas simulasi wawancara berikut, berdasarkan
3 kriteria: (1) kejelasan struktur jawaban, (2) penggunaan contoh konkret,
(3) relevansi jawaban dengan pertanyaan yang diajukan.
Balas dalam format JSON:
{
  "kejelasan": "singkat, 1 kalimat",
  "contoh_konkret": "singkat, 1 kalimat",
  "relevansi": "singkat, 1 kalimat",
  "saran_perbaikan": "1-2 kalimat, nada suportif"
}
Jangan menyatakan kandidat "lulus" atau "tidak lulus" — ini adalah sesi latihan,
bukan keputusan rekrutmen resmi.

Transkrip wawancara:
{{transkrip_lengkap}}
```

### 8.7 Prinsip Umum Prompt Engineering Lintas Agen

Beberapa praktik yang berlaku untuk keenam agen di atas secara umum:

- **Satu agen, satu tanggung jawab**: hindari menggabungkan tugas klasifikasi, retrieval grounding, dan penjawaban ke dalam satu prompt besar — ini menyulitkan debugging di n8n dan meningkatkan risiko output yang tidak konsisten.
- **Output terstruktur untuk agen non-user-facing** (Agen 1, 2, 3, 6): gunakan JSON atau tag XML agar dapat diparse secara andal oleh node n8n berikutnya, dan uji parsing-nya sebagai bagian dari pengujian integrasi (lihat Bagian 6.2).
- **Output percakapan natural untuk agen user-facing** (Agen 4 dan 5): hindari format JSON pada respons yang langsung dibaca pengguna di Streamlit.
- **Sertakan contoh negatif** (hal yang tidak boleh dilakukan) selain contoh positif, terutama untuk Agen 4 dan 5 yang rawan halusinasi atau keluar dari peran.
- **Uji setiap prompt secara terpisah** menggunakan dataset kecil kasus uji (test case) sebelum diintegrasikan ke workflow n8n penuh — ini bisa dimasukkan sebagai bagian dari pengujian unit (Bagian 6.1) dengan memisahkan pengujian "logika prompt" dari "logika kode".
- **Versikan prompt** (prompt versioning) — simpan setiap perubahan system prompt sebagai bagian dari kontrol versi kode, karena perubahan kecil pada prompt dapat berdampak besar pada perilaku agen, sama seperti perubahan kode.

## 9. Catatan Penutup

Dokumen ini bersifat hidup (living document) dan dapat diperbarui seiring perkembangan proyek, terutama pada bagian batasan teknis dan hasil pengujian performa yang mungkin berubah setelah implementasi awal selesai. Disarankan untuk meninjau ulang ruang lingkup ini secara berkala, terutama saat mempertimbangkan penambahan fitur baru seperti dukungan multi-bahasa, integrasi suara, atau peningkatan skala infrastruktur, agar batasan-batasan yang telah ditetapkan di awal tetap konsisten dengan realita kebutuhan proyek yang mungkin berkembang.
