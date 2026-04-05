import streamlit as st
from google import genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Indramayu CLUB - Secure Nur", page_icon="🐉")

# --- 2. MENGAMBIL KUNCI DARI BUNGKUSAN (SECRETS) ---
def get_nur_keys():
    keys = []
    # Mencoba mengambil 4 kunci dari Secrets
    for i in range(1, 5):
        key_name = f"NUR_KEY_{i}"
        if key_name in st.secrets:
            keys.append(st.secrets[key_name])
    return keys

NUR_KEYS = get_nur_keys()

# --- 3. LOGIKA ROTASI OTOMATIS ---
def get_active_client():
    if not NUR_KEYS:
        st.error("🏮 BUNGKUSAN KOSONG: Kunci belum dimasukkan di Secrets.")
        return None, 0
        
    for i, key in enumerate(NUR_KEYS):
        try:
            client = genai.Client(api_key=key)
            # Tes singkat (ping)
            client.models.generate_content(model="gemini-2.0-flash", contents="hi")
            return client, i + 1
        except:
            continue
    return None, 0

client, key_num = get_active_client()

# --- 4. TAMPILAN DASHBOARD ---
st.markdown("""
    <style> .stApp { background-color: #0e1117; } </style>
    <div style="background: linear-gradient(90deg, #4b0082, #8a2be2); padding: 20px; border-radius: 15px; text-align: center; color: white;">
        <h1 style="margin:0;">🐉 INDRAMAYU CLUB</h1>
        <p style="opacity:0.8;">Protokol Keamanan: Env Terbungkus ✅</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. CHAT SYSTEM ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Tanyakan sesuatu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    if client:
        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.warning("Energi Kunci Habis. Mohon Refresh.")
    else:
        st.error("Semua Kunci di dalam bungkus sedang habis kuota.")

# --- 6. MONITOR SIDEBAR ---
with st.sidebar:
    st.header("🛡️ Piramida Guard")
    if client:
        st.success(f"Kunci #{key_num} Beroperasi ✅")
    else:
        st.error("Sistem Offline ❌")
