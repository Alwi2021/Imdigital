import streamlit as st
from google import genai

# --- KUNCI PINTU MASUK (KONFIGURASI) ---
# Kode ini langsung mengambil kunci dari Secrets yang kamu isi tadi
try:
    # Kita buat koneksi 'client' yang memegang kunci API
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Gagal Konfigurasi API: {e}")
    st.stop()

# --- TAMPILAN SISTEM ---
st.title("🌐 Imdigital Core System")
st.write("Sistem Nur Makrifat siap diperintah.")

# Input dari Admin Jamhari
if prompt := st.chat_input("Ketik perintah di sini..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- PROSES BICARA (API CALL) ---
    try:
        # Panggil model Gemini 2.0 Flash (paling stabil untuk saat ini)
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"API Error: {e}")
