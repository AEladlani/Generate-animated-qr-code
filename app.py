import streamlit as st
import segno
import base64
from urllib.request import urlopen
from pathlib import Path
from typing import Optional
import tempfile
import os
from PIL import Image

def generate_animated_qr(data: str, scale: int = 5, background: Optional[str] = None,
    output: str = "qr_code.png"):
    qr = segno.make_qr(data)
    if background:
        # URL background
        if background.startswith("http"):
            bg = urlopen(background)
        else:
            bg = open(background, "rb")
        qr.to_artistic( background=bg, target=output, scale=scale)
    else:
        qr.save(output, scale=scale)

# ---------------- Streamlit UI ---------------- #
#st.set_page_config(page_title="Animated QR Generator", layout="centered")
#logo = Image.open("ANIMATED QR CODE GENERATOR.gif")
#st.image(logo, width=800)
#st.title("Animated QR Code Generator")
st.set_page_config(page_title="Animated QR Generator", layout="centered")
with open("ANIMATED QR CODE GENERATOR.gif", "rb") as f:
    data = f.read()
encoded = base64.b64encode(data).decode()
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/gif;base64,{encoded}" width="900">
    </div>
    """,
    unsafe_allow_html=True)
#st.title("Animated QR Code Generator")
st.write("Generate QR codes with optional image or GIF backgrounds.")
data = st.text_input("📌 Data to encode", placeholder="https://example.com")
scale = st.slider("📏 QR scale", min_value=1, max_value=15, value=5)
use_bg = st.checkbox("Use background")
background_path = None
is_gif = False
if use_bg:
    bg_type = st.radio("Background source", ["Upload file", "From URL"])
    if bg_type == "Upload file":
        uploaded_file = st.file_uploader("🖼 Upload image or GIF",
            type=["png", "jpg", "jpeg", "gif"])
        if uploaded_file:
            suffix = Path(uploaded_file.name).suffix.lower()
            is_gif = suffix == ".gif"
            tmp_bg = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp_bg.write(uploaded_file.read())
            tmp_bg.close()
            background_path = tmp_bg.name
    else:
        bg_url = st.text_input("🌐 Image or GIF URL (ex:https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGkyMXZ4dmgyMzViZnhpbjUzY2ZiaWNtZ293anR6YjFtNHQ0M3llZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3GSoFVODOkiPBFArlu/giphy.gif)", placeholder="https://media.giphy.com/media/LpwBqCorPvZC0/giphy.gif")
        if bg_url:
            is_gif = bg_url.lower().endswith(".gif")
            background_path = bg_url

output_name = st.text_input( "💾 Output filename (without extension)", value="qr_code")

if st.button("🚀 Generate QR Code"):
    if not data:
        st.error("Please enter data to encode.")
    else:
        extension = ".gif" if is_gif else ".png"
        output_file = output_name + extension
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, output_file)
            generate_animated_qr(data=data,scale=scale,
                                 background=background_path,output=output_path)
            st.success("✅ QR code generated!")
            if extension == ".gif":
                st.image(output_path)
            else:
                st.image(output_path)
            with open(output_path, "rb") as f:
                st.download_button( label="⬇️ Download QR code",data=f,
                    file_name=output_file, mime="image/gif" if is_gif else "image/png")
