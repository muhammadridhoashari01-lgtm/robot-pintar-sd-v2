# 🤖 Robot Pintar V2 - Asisten Belajar Interaktif SD

**Robot Pintar V2 (Doni)** adalah aplikasi asisten pembelajaran berbasis kecerdasan buatan (AI) yang dirancang khusus untuk menjadi teman belajar yang interaktif, ceria, dan edukatif bagi siswa Sekolah Dasar (SD) kelas 1 hingga 6 di Indonesia.

Proyek ini dikembangkan sebagai inovasi media pembelajaran digital terpadu yang selaras dengan pendekatan Pendidikan Guru Sekolah Dasar (PGSD). Secara khusus, arsitektur *prompt* pada sistem ini dioptimalkan untuk mendukung sasaran akademik spesifik, seperti penanaman karakter cinta tanah air pada siswa kelas IV SD, terutama melalui pendekatan bercerita (*storytelling*) pada materi Sejarah Kerajaan di Indonesia.

## ✨ Fitur Utama

*   **Antarmuka Ramah Anak:** Desain UI/UX yang ceria, mudah digunakan, dan penuh dengan emoji responsif untuk menjaga semangat belajar siswa.
*   **Kecerdasan Buatan (AI) Terkurasi:** Menggunakan model `google/gemma-4-26b-a4b-it:free` via OpenRouter yang difilter khusus agar tidak memunculkan "teks pemikiran" (reasoning text), sehingga percakapan tetap natural dan fokus pada materi pelajaran.
*   **Suara Otomatis (Text-to-Speech):** Terintegrasi dengan Microsoft Edge TTS (`id-ID-ArdiNeural`) yang membacakan setiap penjelasan AI secara otomatis. Sistem dilengkapi dengan Regex Filter pintar untuk mengabaikan simbol, *markdown*, dan emoji agar suara terdengar layaknya manusia sungguhan.
*   **Memori Percakapan Kontinu:** AI mampu mengingat riwayat obrolan sebelumnya dalam satu sesi, memungkinkan proses tanya-jawab beruntun yang mengalir seperti interaksi dengan guru sungguhan.
*   **Keamanan Terjamin:** Menggunakan *reverse proxy* (Cloudflare Workers) untuk melindungi API Key dan menghindari kendala CORS pada penelusuran web.

## 🛠️ Teknologi yang Digunakan

*   **Frontend & Interaksi:** [Streamlit](https://streamlit.io/) (Python)
*   **AI Engine (LLM):** [OpenRouter API](https://openrouter.ai/) (Model: Gemma 4 26B)
*   **Voice Engine:** `edge-tts` (Microsoft Edge Text-to-Speech)
*   **Backend & Security:** Cloudflare Workers

## 🚀 Panduan Instalasi (Menjalankan di Komputer Sendiri)

Jika Anda ingin menjalankan atau mengembangkan proyek ini di perangkat lokal, ikuti langkah-langkah berikut:

1. **Clone repositori ini:**
   ```bash
   git clone [https://github.com/USERNAME-ANDA/robot-pintar-sd-v2.git](https://github.com/USERNAME-ANDA/robot-pintar-sd-v2.git)
   cd robot-pintar-sd-v2





// Kepada penerus masa depan:
// Saat robot pintar ini dibuat, hanya Tuhan dan saya yang mengerti logikanya.
// Sekarang, hanya Tuhan yang tahu.
// Jika Anda berniat merombak robot pintar ini dan akhirnya eror
// tolong tambahkan pemberitahuan ini sebagai peringatan
 


📋 Proyek ini dikembangkan sebagai inovasi media pembelajaran digital guna meningkatkan motivasi belajar dan menanamkan karakter positif pada siswa Sekolah Dasar.
