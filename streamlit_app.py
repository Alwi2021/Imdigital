import streamlit as st
from google import genai

# Setup Klien dengan API Key dari Secrets
client = genai.Client(api_key=st.secrets[api_key ':=' AIzaSyCH2yiCqUZoceiJvNo1BycDAfKZPuNGKtw':='])

st.title("🐉 Imdigital - Gemini 3 Core")

if prompt := st.chat_input("Perintah untuk 9 Naga..."):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )
    st.write(response.text)
