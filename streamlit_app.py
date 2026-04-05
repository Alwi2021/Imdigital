import streamlit as st
from google import genai

# CARA YANG BENAR DAN BERSIH:
# Kita ambil kunci dari Secrets Streamlit agar aman
try:
    api_key_pusat = st.secrets["AIzaSyCH2yiCqUZoceiJvNo1BycDAfKZPuNGKtw"]
    client = genai.Client(api_key=api_key_pusat)
except Exception as e:
    st.error("Kunci API belum terpasang di Secrets Streamlit.")
    st.stop()

st.title("🐉 Nur Makrifat AI Core")

if prompt := st.chat_input("Perintah Admin..."):
    st.chat_message("user").markdown(prompt)
    
    try:
        # Menggunakan model terbaru gemini-2.0-flash
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        st.chat_message("assistant").markdown(response.text)
    except Exception as e:
        st.error(f"Terjadi gangguan sinyal: {e}")

