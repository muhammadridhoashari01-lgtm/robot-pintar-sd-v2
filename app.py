import streamlit as st
import requests
import asyncio
import base64
import edge_tts
import io
import re

# 1. KONFIGURASI HALAMAN UTAMA (TEMA CERIA RAMAH ANAK)
st.set_page_config(page_title="Robot Pintar V2", page_icon="🤖", layout="centered")

# Menggunakan gambar diam dari rumah GitHub Anda
LINK_GAMBAR_DONI = "doni.png"

# =========================================================================
# 2. ALAMAT BACKEND CLOUDFLARE WORKER ANDA
# =========================================================================
WORKER_URL = "https://purple-surf-7511.muhammadridhoashari01.workers.dev/"
# =========================================================================

# 3. INISIALISASI MEMORI CHAT AGAR RIWAYAT TIDAK HILANG
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FUNGSI GENERATE SUARA MICROSOFT EDGE-TTS (ASYNCHRONOUS) ---
async def generate_edge_audio(text):
    # Menggunakan suara pria Indonesia 'Ardi' yang sangat natural untuk karakter Doni
    VOICE = "id-ID-ArdiNeural"
    communicate = edge_tts.Communicate(text, VOICE)
    
    # Simpan hasil stream audio ke dalam memori
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
            
    return audio_data

# FUNGSI UTAMA SUPAYA SUARA LANGSUNG AUTOPLAY DI WEB
def autoplay_audio(text):
    try:
        # Jalankan fungsi async edge-tts di dalam fungsi biasa Streamlit
        audio_bytes = asyncio.run(generate_edge_audio(text))
        
        # Ubah data audio menjadi format base64 agar bisa di-autoplay oleh HTML5
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Gagal memproses suara: {str(e)}")

# 4. TAMPILAN BANNER UTAMA
st.markdown("<center>", unsafe_allow_html=True)
st.image(LINK_GAMBAR_DONI, width=180)
st.title("🤖 Robot Pintar V2")
st.markdown("### *Halo Teman Pintar! Yuk, Belajar Bersama Doni! 🚀✨*")
st.write("Aku adalah asisten belajarmu yang pintar menguasai semua pelajaran SD kelas 1-6. Mau tanya PR Matematika, IPA, atau dongeng Sejarah Indonesia? Ketik di bawah ya!")
st.markdown("</center><br>", unsafe_allow_html=True)

# Tampilkan Riwayat Obrolan di Layar
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. LOGIKA UTAMA PERCAKAPAN CHAT
if user_input := st.chat_input("Tulis pertanyaan belajarmu di sini..."):
    
    # Tampilkan pertanyaan siswa di layar
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Respon dari Robot Pintar V2
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*Doni sedang membuka buku pintar... ⚡📚*")
        
        system_instruction = (
            "Kamu adalah 'Robot Pintar V2' yang berwujud seorang bocah SD pintar bernama Doni. "
            "Kamu bertugas menjadi asisten belajar interaktif siswa SD kelas 1-6 di Indonesia. "
            "Kuasai semua materi pelajaran SD (IPAS, Matematika, IPS, Sejarah, PPKn) sesuai kurikulum Indonesia.\n\n"
            "ATURAN MENJAWAB:\n"
            "1. Jawab dengan bahasa yang sangat ramah anak, ceria, penuh semangat, dan mudah dipahami.\n"
            "2. Gunakan sapaan variatif di setiap jawaban (contoh: 'Wah hebat!', 'Pertanyaan bagus, teman pintar!').\n"
            "3. Jika materi matematika, jelaskan langkahnya memakai perumpamaan benda (buah/kue).\n"
            "4. Jika materi sejarah, ceritakan seperti dongeng singkat yang seru untuk menanamkan jiwa Cinta Tanah Air.\n"
            "5. Gunakan banyak emoji lucu (🚀, ✨, 🌈, 🧠) dan tebalkan (bold) kata kunci penting."
        )
        
        full_messages = [{"role": "system", "content": system_instruction}] + st.session_state.messages

     payload = {
            # Menggunakan format ID resmi OpenRouter untuk Gemma 4 31B versi gratis
            "model": "google/gemma-4-31b-it:free",
            "messages": full_messages,
            # Pertahankan suhu rendah agar jawaban Doni tetap faktual dan logis
            "temperature": 0.3,
            "max_tokens": 550
        }
        headers = {"Content-Type": "application/json"}

        try:
            target_endpoint = f"{WORKER_URL}/v1/chat/completions" if not WORKER_URL.endswith("/v1/chat/completions") else WORKER_URL
            response = requests.post(target_endpoint, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                # Menggunakan .get() agar tidak langsung error jika 'content' tidak ada
                bot_reply = result["choices"][0]["message"].get("content")
                
                # --- JARING PENGAMAN: JIKA AI SEDANG MELAMUN / JAWABAN KOSONG ---
                if bot_reply is None:
                    bot_reply = "Aduh, maaf ya teman pintar! Pikiran Doni tiba-tiba nge-blank. Bisa tanya sekali lagi? 😅🚀"
                
                # 1. Tampilkan teks jawaban di layar
                message_placeholder.markdown(bot_reply)
                
                # --- PROSES PEMBERSIHAN TEKS KHUSUS UNTUK SUARA ---
                teks_suara = bot_reply.replace("*", "").replace("#", "")
                teks_suara = re.sub(r'[^\w\s,.?!-]', '', teks_suara)
                
                # 2. Jalankan suara otomatis Edge-TTS secara instan
                autoplay_audio(teks_suara)
                
                # 3. Simpan jawaban ke memori chat
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                
            else:
                message_placeholder.markdown(f"❌ Doni agak lelah... (Error Status: {response.status_code})")
                
        except Exception as e:
            message_placeholder.markdown(f"❌ Gagal terhubung ke server backend Doni. ({str(e)})")
