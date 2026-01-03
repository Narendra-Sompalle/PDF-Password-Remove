import streamlit as st
import pikepdf
import io
import time

# Page configuration for a professional look
st.set_page_config(
    page_title="PDF Shield - Unlocker",
    page_icon="🔓",
    layout="centered"
)

# Custom CSS for a modern look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #28a745;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def unlock_pdf(file_bytes, password):
    try:
        with pikepdf.open(file_bytes, password=password) as pdf:
            output_buffer = io.BytesIO()
            pdf.save(output_buffer)
            output_buffer.seek(0)
            return output_buffer, None
    except pikepdf.PasswordError:
        return None, "❌ Incorrect password. Please check and try again."
    except Exception as e:
        return None, f"⚠️ Error: {str(e)}"

# --- Sidebar ---
with st.sidebar:
    st.title("Settings")
    st.info("This tool removes passwords from PDFs using high-grade decryption.")
    st.write("---")
    st.write("🔒 **Security Note:** Your files are processed in memory and never stored on our servers.")

# --- Main UI ---
st.title("🔓 PDF Password Remover")
st.subheader("Fast, Secure, and Universal")

uploaded_file = st.file_uploader("Upload your protected PDF file", type="pdf")

if uploaded_file:
    st.success(f"📄 File uploaded: {uploaded_file.name}")
    password = st.text_input("Enter the PDF Password", type="password", help="Case-sensitive")

    if st.button("Unlock PDF Now"):
        if not password:
            st.warning("Please enter a password.")
        else:
            with st.spinner("🔓 Decrypting your file..."):
                # Simulating a small delay for better UX animation
                time.sleep(1.5)
                result, error = unlock_pdf(uploaded_file, password)
                
                if result:
                    st.balloons() # Visual celebration
                    st.success("✅ Success! Your PDF is now ready for download.")
                    
                    st.download_button(
                        label="⬇️ Download Unlocked PDF",
                        data=result,
                        file_name=f"unlocked_{uploaded_file.name}",
                        mime="application/pdf"
                    )
                else:
                    st.error(error)

# Footer
st.markdown("---")
st.markdown("<center>Built with ❤️ for 100% Accuracy</center>", unsafe_allow_html=True)