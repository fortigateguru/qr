import streamlit as st
import qrcode
from PIL import Image
import io

# Step 1: Generate QR Code with Logo
def generate_qr_with_logo(url, logo_path):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create the QR code image
    img_qr = qr.make_image(fill='black', back_color='white').convert('RGB')
    
    # Open the logo image (Make sure it's small and in PNG format)
    logo = Image.open(logo_path)
    
    # Resize the logo
    logo_size = 50  # Adjust this depending on the size of your QR code
    logo = logo.resize((logo_size, logo_size))
    
    # Position the logo at the center of the QR code
    pos = ((img_qr.size[0] - logo_size) // 2, (img_qr.size[1] - logo_size) // 2)
    img_qr.paste(logo, pos, mask=logo)  # Use the logo as a mask for transparency
    
    # Convert the image to BytesIO for displaying in Streamlit
    img_byte_arr = io.BytesIO()
    img_qr.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

# Step 2: Show QR Code and Instructions
url = "https://datacompare.net"
st.title("Scan the QR Code to Get Device Info")
st.write("Scan the QR code below using your smartphone to see what your device shares with the web.")

# Path to your logo file
logo_path = "your_logo.png"  # Make sure your logo is a PNG file with transparency

# Generate the QR code with logo
qr_code_img = generate_qr_with_logo(url, logo_path)
st.image(qr_code_img, caption="Scan the QR code", use_column_width=True)
