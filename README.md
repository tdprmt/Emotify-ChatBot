# 🚀 Emotify Advanced: Chatbot Literasi Emosi Canggih untuk Remaja

## Deskripsi Singkat

Remaja sering mengalami kesulitan dalam memahami, mengekspresikan, dan mengelola emosinya. Emotify Advanced adalah chatbot edukatif interaktif berbasis AI yang dirancang untuk membantu remaja mengenali jenis emosi yang mereka alami berdasarkan teks yang mereka tulis. Lebih dari itu, Emotify kini dilengkapi dengan berbagai fitur canggih seperti mode curhat bebas (journaling), pelacakan riwayat emosi dengan visualisasi, tantangan interaktif untuk keseimbangan emosi, kamus emosi, sumber aktivitas pendukung, dan ruang refleksi untuk mendukung perjalanan literasi emosi mereka secara menyeluruh.

---

## Fitur Utama

- ✨ **Deteksi Emosi Akurat**: Menggunakan model transformers (`j-hartmann/emotion-english-distilroberta-base`) untuk mengenali emosi dari teks.
- 💬 **Respons Edukatif Bervariasi**: Memberikan tanggapan yang dinamis, edukatif, dan suportif sesuai jenis emosi yang terdeteksi serta kata kunci tertentu.
- ✍️ **Mode Curhat Bebas (Journaling)**: Ruang aman bagi pengguna untuk menuliskan curahan hati tanpa langsung dianalisis, dengan opsi analisis di kemudian waktu.
- 📊 **Riwayat & Peta Emosi Sesi Ini**: Melacak emosi yang terdeteksi selama sesi penggunaan dan menampilkannya dalam bentuk daftar serta grafik visual (bar chart menggunakan Matplotlib) untuk membantu mengenali pola.
- 🎯 **Tantangan Keseimbangan Emosi Interaktif**: Menyediakan daftar tantangan harian yang dapat dicentang pengguna untuk mendorong praktik kesejahteraan emosional, lengkap dengan animasi perayaan (`st.balloons()`) saat semua tantangan selesai.
- 📚 **Kamus Emosi**: Penjelasan singkat mengenai berbagai jenis emosi dasar untuk meningkatkan pemahaman.
- 💡 **Aktivitas & Sumber Bantuan**: Menyediakan saran aktivitas sederhana dan tautan ke sumber informasi kredibel untuk dukungan lebih lanjut.
- 🤔 **Refleksi Minggu Ini**: Kutipan atau pertanyaan reflektif untuk mendorong introspeksi, dengan area teks untuk pengguna menuliskan dan "menyimpan" (dalam sesi) refleksinya.
- 📢 **Fitur Masukan Pengguna**: Memungkinkan pengguna memberikan saran untuk pengembangan Emotify.
- 🖥️ **Antarmuka Interaktif & Ramah Pengguna**: Dibangun dengan Streamlit untuk pengalaman pengguna yang mulus dan menarik, termasuk penggunaan avatar dalam chat.

---

## Cara Menjalankan di Lokal

1.  **Clone repositori ini** (jika sudah ada, pastikan versi terbaru):
    ```bash
    git clone [URL_REPO_ANDA_DI_SINI] # Ganti dengan URL repo GitHub Anda
    cd [NAMA_FOLDER_REPO_ANDA]
    ```

2.  **Buat dan aktifkan environment virtual** (direkomendasikan):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependensi**:
    Pastikan kamu memiliki file `requirements.txt` di root folder proyekmu yang berisi:
    ```txt
    streamlit
    transformers
    torch
    matplotlib
    # collections (Biasanya sudah bagian dari Python standar)
    ```
    Kemudian jalankan:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi**:
    ```bash
    streamlit run nama_file_utama_anda.py
    ```
    *Catatan: Ganti `nama_file_utama_anda.py` dengan nama file Python utama aplikasi Streamlit Anda (misalnya, `emotify_app.py` atau `Emotify Chatbot v4.py`).*

---

## Preview Aplikasi

*(Anda bisa menambahkan screenshot atau GIF dari aplikasi Emotify Advanced di sini. Tunjukkan fitur-fitur seperti input chat, grafik emosi, mode curhat, dan tantangan.)*
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/41bc933c-b209-46f6-921e-dc19ef17f9be" />

---

## Link Deploy

Aplikasi ini dapat diakses secara online melalui:
🔗 **[Link ke Aplikasi Emotify Anda yang Sudah Di-deploy]**
*(Contoh: https://nama-anda-emotify.streamlit.app/)*

---

## Teknologi yang Digunakan

* **Bahasa Pemrograman**: Python
* **Framework UI**: Streamlit
* **Pemrosesan Bahasa Alami (NLP)**:
    * Hugging Face `transformers` (untuk `pipeline` klasifikasi teks)
    * Model AI: `j-hartmann/emotion-english-distilroberta-base`
* **Visualisasi Data**: Matplotlib (untuk grafik "Peta Emosi")
* **Manajemen Dependensi**: `pip` dan `requirements.txt`
* **Lainnya**: `collections.Counter` (untuk menghitung frekuensi emosi)

---

## Potensi Pengembangan di Masa Depan

* Integrasi model NLP yang secara spesifik dilatih atau di-*fine-tune* untuk Bahasa Indonesia untuk meningkatkan akurasi pada input berbahasa Indonesia.
* Fitur penyimpanan data pengguna (dengan izin dan enkripsi, misalnya menggunakan database sederhana seperti SQLite atau layanan cloud) untuk melacak progres emosi jangka panjang.
* Notifikasi atau pengingat untuk tantangan atau refleksi.
* Personalisasi respons atau saran aktivitas berdasarkan riwayat emosi pengguna.
* Ekspor riwayat emosi atau jurnal ke format PDF atau teks.

---

## Kontributor

* Apriyanti
* Putu Eka Permata
