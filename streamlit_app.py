
import streamlit as st
import google.generativeai as genai

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Imdigital - 9 Naga", page_icon="🐉", layout="wide")

# 2. KONFIGURASI AI GEMINI
try:
    # Pakai cara langsung saja kalau belum setting Secrets
    genai.configure(api_key="AIzaSyCH2yiCqUZoceiJvNo1BycDAfKZPuNGKtw")
    model = genai.generativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Terjadi kesalahan sistem: {e}")


# 3. TAMPILAN SIDEBAR (FOLDER 9 NAGA)
st.sidebar.title("📁 Folder 9 Naga") 
menu = st.sidebar.radio("Pilih Dimensi:", [
    "Pusat Kendali", 
    "Log Sistem", 
    "Database Anggota", 
    "Game Makrifat",
    "niaga & servis", 
    " gallery member", 
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
    st.write("Selamat datang di **Indramayu Club Makrifat**. Gunakan perintah suara atau teks untuk menggerakkan sistem.")
    
    # Fitur Chat AI
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Berikan instruksi pusat..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"):
            st.markdown(response.text)

else:
    st.info(f"Halaman **{menu}** sedang disinkronkan dengan database pusat.")
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
