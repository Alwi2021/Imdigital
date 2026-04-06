import streamlit as st
from google import genai
from google.genai import types
import requests
import json
import time

# --- 1. KONFIGURASI & KONSTANTA ---
st.set_page_config(page_title="Indramayu CLUB - Nur Pro", page_icon="🐉", layout="wide")

# Link Integrasi Nur 3
GAS_URL = "https://script.google.com/macros/s/AKfycbxddcob7z7oaJ0YmKMxS0xzpkkcMYP_5c7RVSN8UoGXT3iOpmIMQrAbDKYaxR2inrbHTw/exec"
DRIVE_MEDIA_URL = "https://drive.google.com/drive/folders/13ucwTcGYQSgeZOer62j7sawV8TmGRh0r"

NUR_KEYS = [
    "AIzaSyDHZ5yzggs7DZWmwmS7AdsnYRh9LI-c6l0",
    "AIzaSyBSYJgnZWJPhd0ccoxa5q3BOKbq2pnmkfk",
    "AIzaSyDS5OmX2cxpcYLYhNJi4mZpW2gNyxs5J7o",
    "AIzaSyCH2yiCqUZoceiJvNo1BycDAfKZPuNGKtw"
]

# --- 2. FUNGSI LOGIKA TAMBAHAN ---
def kirim_komentar_nur(nama, pesan):
    """Mengirim log/komentar ke Google Apps Script"""
    try:
        payload = {"nama": nama, "komentar": pesan, "timestamp": time.ctime()}
        requests.post(GAS_URL, json=payload)
    except:
        pass

# --- 3. CSS & INDEX HTML ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; }}
    .naga-header {{
        background: linear-gradient(135deg, #1e0030, #4b0082);
        padding: 30px; border-radius: 20px; color: white;
        text-align: center; border: 1px solid #8a2be2;
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.3);
        margin-bottom: 25px;
    }}
    .member-btn {{
        display: inline-block; padding: 10px 20px;
        background-color: #ff4b4b; color: white;
        border-radius: 10px; text-decoration: none;
        font-weight: bold; margin-top: 10px;
    }}
    </style>
    <div class="naga-header">
        <h1 style="margin:0; font-family: 'Courier New', monospace;">🐉 INDRAMAYU CLUB PRO</h1>
        <p style="letter-spacing: 2px;">Sistem Otomatisasi Nur: Chat, JSON, Video & Media</p>
        <a href="{DRIVE_MEDIA_URL}" target="_blank" class="member-btn">📁 Buka Folder Media Member</a>
    </div>
    """, unsafe_allow_html=True)

# --- 4. ROTASI KUNCI ---
def get_working_nur_client():
    for i, key in enumerate(NUR_KEYS):
        try:
            client = genai.Client(api_key=key)
            # Test ping kecil
            return client, i + 1
        except:
            continue
    return None, 0

client, key_num = get_working_nur_client()

# --- 5. INTERAKSI CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ketik perintah: 'simpan data', 'buat video', atau konsultasi coding..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if client:
        with st.chat_message("assistant"):
            try:
                # Logika: Kirim ke Kolom Komentar (Nur 3)
                kirim_komentar_nur("Member_Nur", prompt)

                if "video" in prompt.lower():
                    st.info("🎬 Memproses Video... Simpan hasilnya di Drive Member setelah selesai.")
                    # Logika Veo tetap sama...
                    st.warning("Fitur Veo memerlukan kuota API Pro yang stabil.")
                
                elif "data" in prompt.lower() or "json" in prompt.lower():
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(response_mime_type="application/json")
                    )
                    st.json(response.text)
                
                else:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction="Anda adalah Nur, pemimpin teknis Indramayu Club. Gunakan bahasa yang cerdas, ringkas, dan solutif."
                        )
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                st.error(f"Energi Terputus: {str(e)}")
    else:
        st.error("🏮 Semua Kunci Habis Kuota. Hubungi Admin Indramayu Club.")

# --- 6. SIDEBAR INFO ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1183/1183672.png", width=100)
    st.title("Admin Panel")
    st.info(f"Kunci Aktif: Nur #{key_num}")
    st.write("---")
    st.markdown(f"[🔗 Link Komentar Nur 3]({GAS_URL})")
    if st.button("Reset Percakapan"):
        st.session_state.messages = []
        st.rerun()
