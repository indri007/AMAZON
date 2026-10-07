# Design System: Modern Material 3 for Langflow-HRD Chatbot

## Tujuan
Dokumen ini mendeskripsikan desain visual dan UX untuk aplikasi HRD chatbot berbasis Streamlit dan Langflow. Fokusnya adalah pada estetika modern Material 3, antarmuka yang bersih, aksesibilitas, dan pengalaman percakapan yang intuitif.

## Prinsip Desain

1. **Kesederhanaan**
   - Antarmuka minimal dengan penggunaan ruang putih yang cukup.
   - Kehadiran elemen visual yang fokus pada konten percakapan.

2. **Material 3**
   - Warna netral dengan aksen lembut.
   - Bentuk rounded corner yang konsisten.
   - Hierarki tipografi yang jelas.

3. **Konsistensi**
   - Gunakan komponen UI ulang seperti kartu pesan, tombol, dan sidebar.
   - Jaga konsistensi jarak antar elemen dan ukuran tipografi.

4. **Aksesibilitas**
   - Kontras warna memadai untuk teks pada latar belakang.
   - Tombol dan kontrol mudah diklik.
   - Informasi error jelas (misalnya koneksi Langflow gagal).

## Brand & Palet Warna

| Token | Warna | Tujuan |
|------|-------|--------|
| `surface` | #F8FAFC | Latar utama halaman |
| `surface-variant` | #E2E7EF | Panel kartu, sidebar |
| `primary` | #0F62FE | Aksen utama, tombol utama |
| `primary-container` | #D0E2FF | Latar tombol/sel terpilih |
| `secondary` | #006D77 | Aksen pendukung, badge |
| `outline` | #C7CAD0 | Garis batas lembut |
| `text-primary` | #102A43 | Teks utama |
| `text-secondary` | #334E68 | Teks pendukung |
| `error` | #DA1E28 | Pesan error |

> Catatan: Warna ini dapat disesuaikan dengan tema HRD internal perusahaan, tetap menjaga tone netral dan profesional.

## Tipografi

- `Display / Heading 4`: 28–32px, bold
- `Heading 6`: 20–24px, medium
- `Subtitle`: 16px, medium
- `Body`: 14px, regular
- `Caption`: 12px, regular

Gunakan font yang modern dan mudah dibaca. Di web, pilihan default `Inter`, `Roboto`, atau `Plus Jakarta Sans` akan sesuai.

## Layout Utama

### 1. Halaman Utama

- Header: judul aplikasi + deskripsi singkat.
- Sidebar kiri: informasi fitur, contoh pertanyaan, tombol aksi.
- Area utama: chat history dan input percakapan.

### 2. Struktur UI

```
+------------------------------------------------------------+
| Header / Judul                                             |
+---------------------+--------------------------------------+ 
| Sidebar Informasi   | Chat utama                           |
| - About             | + welcome message                    |
| - Examples          | + history bubble                     |
| - Reset button      | + chat input area                    |
+---------------------+--------------------------------------+ 
```

### 3. Chat Bubble

- Pesan user: bubble tepi kanan, warna `primary-container` atau putih dengan border.
- Pesan assistant: bubble tepi kiri, warna `surface-variant`.
- Teks respons: `text-primary`.
- Setiap bubble diberi radius 20px.
- Gunakan avatar / icon kecil untuk membedakan peran.

## Komponen UI

### Header
- Judul besar: `Asisten HRD Virtual`
- Subtitle ringkas: `Tanya seputar cuti, gaji, training, KPI, dan rekrutmen.`
- Ikon atau emoji `👥` untuk memberi nuansa manusiawi.

### Sidebar
- Kartu `Tentang` dengan background `surface-variant`
- Daftar contoh pertanyaan (chip atau tombol kecil)
- Tombol `Hapus Riwayat Chat`
- Status kecil atau badge jika perlu informasi runtime.

### Chat History
- Group pesan berurutan.
- Jangan tampilkan timestamp jika tidak diperlukan.

### Input Chat
- Area input `chat_input` lebar penuh.
- Tombol kirim aksen `primary`.
- Placeholder `Ketik pertanyaan Anda di sini...`.

### Notifikasi Error
- Gunakan warna `error` untuk pesan kesalahan.
- Tampilkan sebagai kartu kecil di atas area chat.
- Contoh: `❌ Tidak dapat terhubung ke Langflow. Pastikan Langflow sedang berjalan.`

## Interaksi & UX

### Alur Pengguna
1. Buka aplikasi, baca pengalaman pembuka.
2. Pilih contoh pertanyaan atau ketik sendiri.
3. Kirim chat, tunggu respons dengan animasi spinner.
4. Lihat jawaban di bubble assistant.
5. Reset riwayat jika ingin mulai ulang.

### Feedback pengguna
- Tampilkan spinner selama permintaan berlangsung.
- Feedback cepat saat tombol ditekan.
- Pesan error jelas, hindari teks teknis.

## Modern Material 3 Adaptasi di Streamlit

Streamlit tidak memiliki komponen Material 3 resmi, tetapi prinsipnya bisa diaplikasikan dengan:
- `st.set_page_config` untuk judul dan layout.
- `st.container` / `st.columns` untuk struktur.
- `st.markdown` dengan CSS inline minimal untuk styling bubble.
- `st.button` untuk contoh pertanyaan dan reset.

### Contoh gaya CSS sederhana

Gunakan `st.markdown` bersama style:

```python
st.markdown(
    """
    <style>
    .chat-bubble {
      border-radius: 18px;
      padding: 16px;
      margin-bottom: 12px;
      box-shadow: 0 1px 2px rgba(16, 42, 67, 0.08);
      max-width: 770px;
    }
    .user-bubble { background: #E8F1FF; color: #102A43; }
    .assistant-bubble { background: #F1F5F9; color: #102A43; }
    .sidebar-card { background: #E2E7EF; border-radius: 18px; padding: 18px; }
    </style>
    """,
    unsafe_allow_html=True,
)
```

## Rekomendasi Pengembangan Visual

- Gunakan `st.chat_message` untuk struktur percakapan tetapi tambahkan styling khusus bila memungkinkan.
- Pilih icon sederhana untuk avatar: `🧑` untuk pengguna, `👥` untuk assistant.
- Jaga voice aplikasi tetap sopan, profesional, dan membantu.

## Rencana Desain

1. Terapkan palet warna dan tipografi di `design.md`.
2. Perbarui `streamlit_app.py` dengan layout dua kolom dan kartu sidebar.
3. Tambahkan style bubble minimal untuk tampilan lebih modern.
4. Pertimbangkan transisi pada spinner / response loading.
5. Testing UX: keyboard input, reset chat, dan error copy.

## Kesimpulan
Desain ini dibuat untuk memperkuat pengalaman HRD chatbot sebagai aplikasi percakapan profesional, modern, dan mudah dipakai. Fokus utama adalah percakapan, kejelasan, dan konsistensi visual dengan prinsip Material 3.
