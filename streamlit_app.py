import streamlit as st
from google import genai

# --- 1. KONFIGURASI HALAMAN (LAYOUT) ---
st.set_page_config(
    page_title="Indramayu Club Makrifat",
    page_icon="🐉",
    layout="centered"
)

# --- 2. CSS CUSTOM (PENGGANTI INDEX.HTML) ---
# Ini adalah bagian untuk mempercantik tampilan agar tidak kaku
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTitle {
        color: #00ffcc;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 2px 2px #000;
    }
    .naga-header {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_state_ Wood=True)

# --- 3. KONEKSI KE GEMINI (AMBIL DARI SECRETS) ---
try:
    # Mengambil kunci rahasia yang sudah kamu pasang di dashboard
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("⚠️ Koneksi Pusat Terputus: Periksa Secrets di Streamlit.")
    st.stop()

# --- 4. HEADER VISUAL ---
st.markdown("""
    <div class="naga-header">
        <h1>🐉 INDRAMAYU CLUB MAKRIFAT</h1>
        <p>Pusat Kendali Digital - Nur Makrifat Core</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. LOGIKA CHAT (MEMORI SISTEM) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Selamat datang Admin Jamhari. Sistem Nur Makrifat siap diperintah secara global."}
    ]

# Menampilkan riwayat percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. INPUT PERINTAH (GEMINI 3 FLASH) ---
if prompt := st.chat_input("Berikan instruksi pusat..."):
    # Simpan input user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Memanggil mesin Gemini terbaru sesuai riset kamu
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        
        # Tampilkan jawaban AI
        answer = response.text
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
            
    except Exception as e:
        st.error(f"❌ Gangguan Dimensi: {e}")

# --- 7. FOOTER ---
st.markdown("---")
st.caption("© 2026 Indramayu Club Makrifat | Powered by Gemini 3 Flash")
