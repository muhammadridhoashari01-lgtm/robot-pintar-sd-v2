import streamlit as st
import requests
from gtts import gTTS
import base64
import io

# 1. KONFIGURASI HALAMAN UTAMA (TEMA CERIA RAMAH ANAK)
st.set_page_config(page_title="Robot Pintar V2", page_icon="🤖", layout="centered")

# Variabel Global URL Karakter Bocah SD Anda dari Postimages
LINK_GAMBAR_DONI = "doni.png"

# =========================================================================
# 2. ALAMAT BACKEND CLOUDFLARE WORKER BARU ANDA
# Ganti URL di dalam tanda kutip di bawah dengan URL Worker baru (robot-pintar-backend) Anda!
# =========================================================================
WORKER_URL = "https://purple-surf-7511.muhammadridhoashari01.workers.dev"
# =========================================================================

# FUNGSI AGAR SUARA DONI LANGSUNG BUNYI OTOMATIS SAAT CHAT MUNCUL
def autoplay_audio(text):
    try:
        tts = gTTS(text=text, lang='id', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # Mengubah file suara menjadi kode base64 agar bisa disuntikkan ke HTML
        b64 = base64.b64encode(fp.read()).decode()
        
        # Trik HTML5 Autoplay yang disuntikkan secara rahasia ke dalam web
        audio_html = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        pass

# 3. TAMPILAN BANNER UTAMA (MEMANGGIL KARAKTER BOCAH SD ANDA)
st.markdown("<center>", unsafe_allow_html=True)
st.image(LINK_GAMBAR_DONI, width=180)
st.title("🤖 Robot Pintar V2")
st.markdown("### *Halo Teman Pintar! Yuk, Belajar Bersama Doni! 🚀✨*")
st.write("Aku adalah asisten belajarmu yang pintar menguasai semua pelajaran SD kelas 1-6. Mau tanya PR Matematika, IPA, atau dongeng Sejarah Indonesia? Ketik di bawah ya!")
st.markdown("</center><br>", unsafe_allow_html=True)

# 4. INISIALISASI MEMORI CHAT ATAR TIDAK HILANG
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan Riwayat Obrolan Sebelum-sebelumnya di Layar
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. LOGIKA KOTAK INPUT UTAMA CHAT ANAK SD
if user_input := st.chat_input("Tulis pertanyaan belajarmu di sini..."):
    from streamlit_mic_recorder import mic_recorder

st.write("Orang tua/Siswa bisa tekan tombol di bawah jika malas mengetik:")
audio_input = mic_recorder(
    start_prompt="🎙️ Mulai Bicara (Doni Mendengarkan)",
    stop_prompt="🛑 Selesai Bicara",
    key='recorder'
)

# Jika anak selesai merekam suara
if audio_input:
    # Di sini kita butuh API eksternal (seperti OpenAI Whisper) untuk mengubah suara menjadi teks.
    # Untuk prototipe awal skripsi, kita fokuskan suara keluar (Doni bicara) dulu agar sistem Cloudflare-nya stabil ya!
    st.info("Suara Anda berhasil direkam! Fitur pengubah suara ke teks (Speech-to-Text) sedang dihubungkan.")
    
    # Tampilkan pertanyaan siswa di layar
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Respon dari Robot Pintar V2
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*Doni sedang membuka buku pintar... ⚡📚*")
        
        # PROMPT UTAMA GURU SD YANG CERIA & VARIATIF
        system_instruction = (
            "Kamu adalah 'Robot Pintar V2' yang berwujud seorang bocah SD pintar bernama Doni. "
            "Kamu bertugas menjadi asisten belajar interaktif siswa SD kelas 1-6 di Indonesia. "
            "Kuasai semua materi pelajaran SD (IPAS, Matematika, IPS, Sejarah, PPKn) sesuai kurikulum Indonesia.\n\n"
            "ATURAN MENJAWAB:\n"
            "1. Jawab dengan bahasa yang sangat ramah anak, ceria, penuh semangat, dan mudah dipahami.\n"
            "2. Gunakan sapaan variatif di setiap jawaban (contoh: 'Wah hebat!', 'Pertanyaan bagus, teman pintar!', 'Yuk kita bedah!').\n"
            "3. Jika materi matematika, jelaskan langkahnya memakai perumpamaan benda (buah/kue), jangan langsung hasil akhir.\n"
            "4. Jika materi sejarah, ceritakan seperti dongeng singkat yang seru untuk menanamkan jiwa Cinta Tanah Air.\n"
            "5. Gunakan banyak emoji lucu (🚀, ✨, 🌈, 🧠, 📐) dan tebalkan (bold) kata kunci penting.\n"
            "6. JANGAN memberikan jawaban yang sama persis jika ditanya berulang kali. Gunakan variasi kosakata baru agar anak tidak bosan."
        )
        
        full_messages = [{"role": "system", "content": system_instruction}] + st.session_state.messages

        payload = {
            "model": "openai/gpt-oss-120b:free",
            "messages": full_messages,
            "temperature": 0.9, # Disetel tinggi agar jawaban bervariasi dan tidak monoton
            "max_tokens": 550
        }
        
        headers = {
            "Content-Type": "application/json"
        }

        try:
            # Kirim data chat ke tameng Cloudflare Worker baru
            target_endpoint = f"{WORKER_URL}/v1/chat/completions" if not WORKER_URL.endswith("/v1/chat/completions") else WORKER_URL
            response = requests.post(target_endpoint, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                bot_reply = result["choices"][0]["message"]["content"]
                
                # Tampilkan tulisan teks jawaban di layar web
                message_placeholder.markdown(bot_reply)
                
                # JALANKAN SUARA SUARA OTOMATIS BERBAHASA INDONESIA
                autoplay_audio(bot_reply)
                
                # Simpan jawaban ke riwayat memori
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            else:
                message_placeholder.markdown(f"❌ Doni agak lelah... (Error Status: {response.status_code})")
                
        except Exception as e:
            message_placeholder.markdown(f"❌ Gagal terhubung ke server backend Doni. ({str(e)})")
