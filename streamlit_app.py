import streamlit as st
from google import genai
from google.genai import types

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Indramayu CLUB - Nur AI",
    page_icon="🐉",
    layout="centered"
)

# --- 2. CSS CUSTOM (NUANSA UNGU & MODERN) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .naga-header {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    </style>
    <div class="naga-header">
        <h1 style="margin:0;">🐉 INDRAMAYU CLUB</h1>
        <p style="opacity:0.8; margin:5px 0 0 0;">Protokol Nur 7: Komunikasi Makrifat</p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. KONEKSI KE GEMINI ---
def get_client():
    try:
        # Mengambil API Key dari Secrets
        api_key = st.secrets["GEMINI_API_KEY"]
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error("⚠️ Koneksi Pusat Terputus: Periksa Secrets 'GEMINI_API_KEY' di Streamlit.")
        return None

client = get_client()

# --- 4. LOGIKA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input User
if prompt := st.chat_input("Tanyakan sesuatu pada Nur..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if client:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Memanggil AI
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                full_response = response.text
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    st.warning("🏮 **Nur sedang bermeditasi (Kuota Habis).** Mohon tunggu beberapa saat atau gunakan kunci API lain.")
                else:
                    st.error(f"Sistem Error: {error_msg}")
