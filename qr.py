import streamlit as st
import qrcode
from PIL import Image
import streamlit.components.v1 as components

# Step 1: Generate Regular QR Code
def generate_qr_code(url):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create the QR code image
    img_qr = qr.make_image(fill='black', back_color='white')
    
    return img_qr

# Step 2: Show QR Code and Instructions
url = "https://qrcodeinfo.streamlit.app"
st.title("Scan the QR Code to Get Device Info")
st.write("Welcome! Scan the QR code below using your smartphone to see what your device shares with the web.")

# Generate the QR code
qr_code_img = generate_qr_code(url)
st.image(qr_code_img, caption="Scan the QR code")

# Step 3: Theme Toggle
theme = st.radio("Choose a theme", ("Light", "Dark"))

# Apply background color based on theme
if theme == "Dark":
    bg_color = "#333333"
    text_color = "#FFFFFF"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"

# Apply theme styles
st.markdown(f"""
    <style>
    body {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .stButton > button {{
        background-color: #4CAF50;
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

# Step 4: Use components.html to run JS and display device info
components.html(f"""
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <style>
            .card {{
                background-color: white;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }}
            .card-dark {{
                background-color: #2C2C2C;
                color: #FFFFFF;
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

        <div class="card { 'card-dark' if theme == 'Dark' else '' }">
            <i class="fa fa-mobile-alt"></i> <strong>User Agent:</strong>
            <p id="user_agent"></p>
        </div>

        <div class="card { 'card-dark' if theme == 'Dark' else '' }">
            <button onclick="toggleVisibility('battery_info')">Show/Hide Battery Info</button>
            <div id="battery_info" style="display:none;">
                <p><i class="fa fa-battery-half"></i> <strong>Battery Level:</strong> <span id="battery_level"></span></p>
                <p><strong>Charging:</strong> <span id="battery_charging"></span></p>
            </div>
        </div>

        <div class="card { 'card-dark' if theme == 'Dark' else '' }">
            <i class="fa fa-wifi"></i> <strong>Network Info:</strong>
            <p id="network_info"></p>
        </div>

        <div class="card { 'card-dark' if theme == 'Dark' else '' }">
            <i class="fa fa-desktop"></i> <strong>Screen Info:</strong>
            <p id="screen_info"></p>
        </div>

        <div class="card { 'card-dark' if theme == 'Dark' else '' }">
            <i class="fa fa-clock"></i> <strong>Time Zone:</strong>
            <p id="timezone_info"></p>
        </div>

        <script>
            function toggleVisibility(id) {{
                var elem = document.getElementById(id);
                if (elem.style.display === "none") {{
                    elem.style.display = "block";
                }} else {{
                    elem.style.display = "none";
                }}
            }}

            // Get user agent
            document.getElementById('user_agent').innerHTML = navigator.userAgent;

            // Get battery info if supported
            if ('getBattery' in navigator) {{
                navigator.getBattery().then(function(battery) {{
                    document.getElementById('battery_level').innerHTML = (battery.level * 100) + "%";
                    document.getElementById('battery_charging').innerHTML = battery.charging ? "Yes" : "No";
                }});
            }} else {{
                document.getElementById('battery_info').innerHTML = "Battery info not available.";
            }}

            // Get network info
            if ('connection' in navigator) {{
                let connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
                document.getElementById('network_info').innerHTML = connection.effectiveType;
            }} else {{
                document.getElementById('network_info').innerHTML = "Network info not available.";
            }}

            // Get screen info
            document.getElementById('screen_info').innerHTML = window.screen.width + "x" + window.screen.height + ", " + window.screen.colorDepth + " bits";

            // Get time zone
            document.getElementById('timezone_info').innerHTML = Intl.DateTimeFormat().resolvedOptions().timeZone;

            // Hide loading message after info is loaded
            document.getElementById('loading_message').style.display = "none";
        </script>
    </body>
    </html>
    """, height=700)
