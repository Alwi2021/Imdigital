import streamlit as st
from google import genai
from google.genai import types
import requests
import json
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Indramayu CLUB - Nur Pro", page_icon="🐉", layout="wide")

# --- 2. MENGAMBIL KUNCI DARI SECRETS ---
# Script ini sekarang otomatis mengambil kunci dari yang Anda input di gambar tadi
try:
    NUR_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Kunci 'GEMINI_API_KEY' tidak ditemukan di Secrets Streamlit!")
    st.stop()

# --- 3. CSS & HEADER ---
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
    </style>
    <div class="naga-header">
        <h1 style="margin:0;">🐉 INDRAMAYU CLUB PRO</h1>
        <p>Sistem Aktif dengan Pengamanan Secrets</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. INISIALISASI CLIENT ---
def get_nur_client():
    try:
        client = genai.Client(api_key=NUR_API_KEY)
        return client
    except Exception as e:
        st.error(f"Gagal inisialisasi: {e}")
        return None

client = get_nur_client()

# --- 5. LOGIKA CHAT ---
# (Lanjutkan dengan logika chat sebelumnya, gunakan objek 'client' di sini)
if prompt := st.chat_input("Ketik perintah Nur..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if client:
        # Contoh respon sederhana
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        with st.chat_message("assistant"):
            st.markdown(response.text)
