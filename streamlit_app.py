import streamlit as st
from google import genai
from google.genai import types
import json
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Indramayu CLUB - Nur Pro", page_icon="🐉", layout="wide")

# --- 2. DAFTAR KUNCI ENERGI (ROTASI) ---
NUR_KEYS = [
    import streamlit as st
from google import genai]

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
# --- 3. CSS MAKRIFAT ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .naga-header {
        background: linear-gradient(135deg, #4b0082, #8a2be2);
        padding: 25px; border-radius: 15px; color: white;
        text-align: center; margin-bottom: 20px;
    }
    </style>
    <div class="naga-header">
        <h1 style="margin:0;">🐉 INDRAMAYU CLUB PRO</h1>
        <p style="opacity:0.8;">Sistem Otomatisasi Nur: Chat, JSON, & Video</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. FUNGSI ROTASI OTOMATIS ---
def get_working_nur_client():
    for i, key in enumerate(NUR_KEYS):
        try:
            client = genai.Client(api_key=key)
            client.models.generate_content(model="gemini-2.0-flash", contents="hi")
            return client, i + 1
        except:
            continue
    return None, 0

client, key_num = get_working_nur_client()

# --- 5. LOGIKA CHAT & PERINTAH ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ketik perintah (contoh: 'buat video naga' atau 'data member')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if client:
        with st.chat_message("assistant"):
            try:
                # CEK APAKAH USER MINTA VIDEO
                if "video" in prompt.lower():
                    st.info("🎬 Nur sedang memproses Manifestasi Video... Mohon tunggu.")
                    operation = client.models.generate_videos(
                        model='veo-3.1-lite-generate-preview',
                        prompt=prompt,
                        config={'numberOfVideos': 1, 'resolution': '720p'}
                    )
                    while not operation.done:
                        time.sleep(5)
                        operation = client.operations.get_videos_operation(operation=operation)
                    video_url = operation.response.generatedVideos[0].video.uri
                    st.video(video_url)
                    st.session_state.messages.append({"role": "assistant", "content": f"Video berhasil dibuat: {video_url}"})
                
                # CEK APAKAH USER MINTA DATA (JSON)
                elif "data" in prompt.lower() or "json" in prompt.lower():
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(response_mime_type="application/json")
                    )
                    st.json(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": "Data JSON ditampilkan."})
                
                # CHAT BIASA (JAGO CODING)
                else:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction="Anda adalah Nur, pakar coding dan spiritual Indramayu Club. Berikan solusi teknis yang jago dan bijak."
                        )
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                st.error(f"Energi Kunci #{key_num} bermasalah: {str(e)}")
    else:
        st.error("🏮 Semua Kunci Habis Kuota.")

# --- 6. SIDEBAR MONITOR ---
with st.sidebar:
    st.header("⚙️ Status Nur Pro")
    st.success(f"Kunci #{key_num} Aktif ✅")
    if st.button("Bersihkan Memori"):
        st.session_state.messages = []
        st.rerun()
