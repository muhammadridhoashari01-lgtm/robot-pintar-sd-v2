import streamlit as st
import requests
from gtts import gTTS
import base64
import io
import re  # Pustaka tambahan untuk membersihkan simbol gaib (Regular Expression)

# 1. KONFIGURASI HALAMAN UTAMA (TEMA CERIA RAMAH ANAK)
st.set_page_config(page_title="Robot Pintar V2", page_icon="🤖", layout="centered")

# Menggunakan gambar diam yang sudah Anda upload di rumah GitHub Anda
LINK_GAMBAR_DONI = "doni.png"

# =========================================================================
# 2. ALAMAT BACKEND CLOUDFLARE WORKER ANDA
# =========================================================================
WORKER_URL = "https://purple-surf-7511.muhammadridhoashari01.workers.dev"
# =========================================================================

# 3. INISIALISASI MEMORI CHAT AGAR RIWAYAT TIDAK HILANG
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FUNGSI PEMBERSIH TEKS GAIB SEBELUM JADI SUARA ---
def bersihkan_teks_untuk_suara(teks):
    try:
        # 1. Hapus tanda bintang (pembuka/penutup bold: ***)
        teks_bersih = re.sub(r'\*', '', teks)
        
        # 2. Hapus tanda hubung pada kata ulang (ganti jadi spasi agar dibaca lancar)
        # Contoh: 'anak-anak' jadi 'anak anak'
        teks_bersih = re.sub(r'-', ' ', teks_bersih)
        
        # 3. Hapus emoji (karakter khusus Unicode)
        # Ini penting agar gTTS tidak bingung membaca simbol gambar
        teks_bersih = re.sub(r'[^\x00-\x7F]+', ' ', teks_bersih)
        
        # 4. Hapus spasi berlebihan
        teks_bersih = re.sub(r'\s+', ' ', teks_bersih).strip()
        
        return teks_bersih
    except:
        return teks # Jika gagal bersihkan, kembalikan teks asli

# FUNGSI SUPAYA SUARA DONI LANGSUNG BUNYI OTOMATIS SAAT JAWABAN MUNCUL
def autoplay_audio(text_asli):
    try:
        # ⚡ LANGKAH VITAL: Bersihkan teks dulu sebelum dikirim ke mesin gTTS
        teks_siap_baca = bersihkan_teks_untuk_suara(text_asli)
        
        # Kirim teks bersih ke mesin gTTS
        tts = gTTS(text=teks_siap_baca, lang='id', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        b64 = base64.b64encode(fp.read()).decode()
        audio_html = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        pass

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
        
        # PROMPT UTAMA GURU SD (Meminta AI memberikan emoji)
        system_instruction = (
            "Kamu adalah 'Robot Pintar V2' yang berwujud seorang bocah SD pintar bernama Doni. "
            "Kamu bertugas menjadi asisten belajar interaktif siswa SD kelas 1-6 di Indonesia. "
            "Kuasai semua materi pelajaran SD (IPAS, Matematika, IPS, Sejarah, PPKn) sesuai kurikulum Indonesia.\n\n"
            "ATURAN MENJAWAB:\n"
            "1. Jawab dengan bahasa yang sangat ramah anak, ceria, penuh semangat, dan mudah dipahami.\n"
            "2. Gunakan sapaan variatif di setiap jawaban (contoh: 'Wah hebat!', 'Pertanyaan bagus!').\n"
            "3. Jika materi sejarah, ceritakan seperti dongeng singkat untuk menanamkan jiwa Cinta Tanah Air.\n"
            "4. Gunakan emoji lucu (🚀, ✨, 🌈, 🧠) dan tebalkan (bold: ***) kata kunci penting.\n"
            "5. Teks di layar harus ada emojinya, tapi jangan khawatir nanti suaranya akan dibersihkan."
        )
        
        full_messages = [{"role": "system", "content": system_instruction}] + st.session_state.messages

        payload = {
            "model": "openai/gpt-oss-120b:free",
            "messages": full_messages,
            "temperature": 0.9,
            "max_tokens": 550
        }
        
        headers = {"Content-Type": "application/json"}

        try:
            target_endpoint = f"{WORKER_URL}/v1/chat/completions" if not WORKER_URL.endswith("/v1/chat/completions") else WORKER_URL
            response = requests.post(target_endpoint, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                bot_reply = result["choices"][0]["message"]["content"]
                
                # 1. Tampilkan teks jawaban di layar (Masih ada emojinya, biar visual anak senang)
                message_placeholder.markdown(bot_reply)
                
                # 2. Jalankan suara otomatis secara instan (Di dalam fungsi ini teks akan dibersihkan otomatis)
                autoplay_audio(bot_reply)
                
                # 3. Simpan jawaban ke memori chat
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                
            else:
                message_placeholder.markdown(f"❌ Doni agak lelah... (Error Status: {response.status_code})")
                
        except Exception as e:
            message_placeholder.markdown(f"❌ Gagal terhubung ke server backend Doni. ({str(e)})")
