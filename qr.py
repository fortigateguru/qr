import streamlit as st
import qrcode
from PIL import Image
import io
import requests
import streamlit.components.v1 as components  # Ensure this import is present

# Step 1: Generate QR Code with Logo from URL
def generate_qr_with_logo(url, logo_url):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create the QR code image
    img_qr = qr.make_image(fill='black', back_color='white').convert('RGB')
    
    # Fetch the logo image from the URL
    response = requests.get(logo_url)
    logo = Image.open(io.BytesIO(response.content))
    
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
url = "https://qrcodeinfo.streamlit.app/"  # Updated Streamlit app URL
st.title("Scan the QR Code to Get Device Info")
st.write("Scan the QR code below using your smartphone to see what your device shares with the web.")

# URL to your logo file
logo_url = "https://github.com/fortigateguru/qr/blob/main/anonymous-8291223_640.png?raw=true"  # URL to your logo

# Generate the QR code with logo from URL
qr_code_img = generate_qr_with_logo(url, logo_url)
st.image(qr_code_img, caption="Scan the QR code", use_column_width=True)

# Step 3: Use components.html to run JS and display device info
components.html(f"""
    <html>
    <head>
        <style>
            .card {{
                background-color: white;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }}
            .loading {{
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="loading" id="loading_message">Fetching your device info...</div>

        <div class="card">
            <strong>User Agent:</strong>
            <p id="user_agent"></p>
        </div>

        <div class="card">
            <strong>Battery Info:</strong>
            <p id="battery_info"></p>
        </div>

        <div class="card">
            <strong>Network Info:</strong>
            <p id="network_info"></p>
        </div>

        <div class="card">
            <strong>Screen Info:</strong>
            <p id="screen_info"></p>
        </div>

        <div class="card">
            <strong>Orientation Info:</strong>
            <p id="orientation_info"></p>
        </div>

        <div class="card">
            <strong>Motion Info:</strong>
            <p id="motion_info"></p>
        </div>

        <div class="card">
            <strong>Touch Support:</strong>
            <p id="touch_support"></p>
        </div>

        <script>
            // Get user agent
            document.getElementById('user_agent').innerHTML = navigator.userAgent;

            // Get battery info if supported
            if ('getBattery' in navigator) {{
                navigator.getBattery().then(function(battery) {{
                    document.getElementById('battery_info').innerHTML = "Level: " + (battery.level * 100) + "%, Charging: " + (battery.charging ? "Yes" : "No");
                }});
            }}

            // Get network info
            if ('connection' in navigator) {{
                let connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
                document.getElementById('network_info').innerHTML = 
                    "Effective Type: " + connection.effectiveType + 
                    ", Downlink: " + connection.downlink + " Mbps, " + 
                    "RTT: " + connection.rtt + " ms";
            }}

            // Get screen info
            document.getElementById('screen_info').innerHTML = window.screen.width + "x" + window.screen.height + ", " + window.screen.colorDepth + " bits";

            // Get orientation info
            window.addEventListener("deviceorientation", function(event) {{
                document.getElementById('orientation_info').innerHTML = "Alpha (Z-axis): " + event.alpha + ", Beta (X-axis): " + event.beta + ", Gamma (Y-axis): " + event.gamma;
            }});

            // Get motion info
            window.addEventListener("devicemotion", function(event) {{
                document.getElementById('motion_info').innerHTML = "Acceleration X: " + event.acceleration.x + ", Y: " + event.acceleration.y + ", Z: " + event.acceleration.z;
            }});

            // Touch support
            let touchSupport = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
            document.getElementById('touch_support').innerHTML = touchSupport ? "Yes" : "No";

            // Hide loading message after info is loaded
            document.getElementById('loading_message').style.display = "none";
        </script>
    </body>
    </html>
    """, height=800)
