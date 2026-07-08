# app.py
import streamlit as st
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="QR Code Generator", layout="centered")

st.title("📱 QR Code Generator")
st.write("Paste a URL or text below, tweak options, then download or save the QR image.")

# --- Inputs ---
text = st.text_area("URL or text to encode", value=" ")
cols = st.columns(3)
with cols[0]:
    box_size = st.number_input("Box size (pixels)", min_value=1, max_value=40, value=10)
with cols[1]:
    border = st.number_input("Border (boxes)", min_value=0, max_value=10, value=4)
with cols[2]:
    ec = st.selectbox("Error correction", options=["L (7%)","M (15%)","Q (25%)","H (30%)"], index=1)

fill_color = st.color_picker("Foreground color", "#000000")
back_color = st.color_picker("Background color", "#FFFFFF")
format_opt = st.selectbox("Image format", options=["PNG","JPEG"], index=0)

# Map selection to qrcode constant
ec_map = {
    "L (7%)": ERROR_CORRECT_L,
    "M (15%)": ERROR_CORRECT_M,
    "Q (25%)": ERROR_CORRECT_Q,
    "H (30%)": ERROR_CORRECT_H,
}
error_correction = ec_map[ec]

# Generate QR
if st.button("Generate QR"):
    if not text.strip():
        st.error("Please enter some text or a URL to encode.")
    else:
        qr = qrcode.QRCode(
            version=None,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

        # Show image
        st.image(img, caption="Generated QR code", use_column_width=False)

        # Prepare in-memory bytes for download
        buf = BytesIO()
        img.save(buf, format=format_opt)
        byte_im = buf.getvalue()

        st.download_button(
            label="Download QR image",
            data=byte_im,
            file_name=f"qr_code.{format_opt.lower()}",
            mime=f"image/{format_opt.lower()}",
        )

        # Optional: save to disk on server (uncomment if needed)
        # with open("my_web.png", "wb") as f:
        #     f.write(byte_im)
        # st.success("Saved to my_web.png on server (if allowed).")
