import streamlit as st
import google.generativeai as genai

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Imdigital - 9 Naga", page_icon="🐉", layout="wide")

# 2. KONFIGURASI AI GEMINI (DIPERBAIKI)
# Kita buat model di luar agar tidak menyebabkan 'name not defined'
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Kunci API 'GEMINI_API_KEY' tidak ditemukan di Secrets Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Menggunakan nama model yang paling stabil
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Gagal inisialisasi model: {e}")
    st.stop()

# 3. TAMPILAN SIDEBAR (FOLDER 9 NAGA)
st.sidebar.title("📁 Folder 9 Naga")
menu = st.sidebar.radio("Pilih Dimensi:", [
    "Pusat Kendali", 
    "Log Sistem", 
    "Database Anggota", 
    "Game Makrifat",
    "niaga & servis",
    "gallery member",
    "Radar Global",
    "Finansial",
    "Konten Kreatif",
    "Keamanan",
    "Gerbang Utama"
])

# 4. TAMPILAN UTAMA (INDEX)
st.title("🌐 Imdigital Core System")
st.markdown(f"### Dimensi: {menu}")

if menu == "Pusat Kendali":
    st.write("Selamat datang di **Indramayu Club Makrifat**. Gunakan perintah teks untuk menggerakkan sistem.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Berikan instruksi pusat..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Menggunakan stream=False agar lebih stabil di HP
            response = model.generate_content(prompt)
            if response.text:
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant"):
                    st.markdown(response.text)
        except Exception as e:
            st.error(f"Sistem gagal merespon: {e}")

else:
    st.info(f"Halaman **{menu}** sedang dalam proses sinkronisasi database.")
