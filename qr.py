import streamlit as st
import qrcode
from PIL import Image
import io
import requests
import streamlit.components.v1 as components

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
    logo_size = 130
    logo = logo.resize((logo_size, logo_size))
    
    # Position the logo at the center of the QR code
    pos = ((img_qr.size[0] - logo_size) // 2, (img_qr.size[1] - logo_size) // 2)
    img_qr.paste(logo, pos, mask=logo)
    
    # Convert the image to BytesIO for displaying in Streamlit
    img_byte_arr = io.BytesIO()
    img_qr.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

# Step 2: Show QR Code and Instructions (In Hebrew)
url = "https://qrcodeinfo.streamlit.app/"
st.title("סרוק את קוד ה-QR כדי לקבל מידע על המכשיר שלך")
st.write("סרוק את קוד ה-QR בעזרת הסמארטפון שלך כדי לראות איזה מידע המכשיר שלך משתף עם האתר.")

# URL to your logo file
logo_url = "https://github.com/fortigateguru/qr/blob/main/anonymous-8291223_640.png?raw=true"

# Generate the QR code with logo from URL
qr_code_img = generate_qr_with_logo(url, logo_url)
st.image(qr_code_img, caption="סרוק את קוד ה-QR", use_column_width=True)

# Step 3: Countdown Timer for Data Collection (In Hebrew)
import time

with st.spinner("אוסף מידע על המכשיר בעוד 5 שניות..."):
    countdown_time = 5
    for i in range(countdown_time, 0, -1):
        st.write(f"אוסף מידע בעוד {i} שניות...")
        time.sleep(1)

st.success("איסוף המידע הושלם! מציג כעת את המידע על המכשיר שלך...")

# Step 4: Use components.html to run JS and display device info, set cookies, and display the cookie value (In Hebrew)
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
        <div class="loading" id="loading_message">אוסף מידע על המכשיר שלך...</div>

        <div class="card">
            <strong>סוכן המשתמש (User Agent):</strong>
            <p id="user_agent"></p>
        </div>

        <div class="card">
            <strong>מידע על הסוללה:</strong>
            <p id="battery_info"></p>
        </div>

        <div class="card">
            <strong>מידע על הרשת:</strong>
            <p id="network_info"></p>
        </div>

        <div class="card">
            <strong>מידע על המסך:</strong>
            <p id="screen_info"></p>
        </div>

        <div class="card">
            <strong>סיכון לזיהוי באמצעות טביעת אצבע דיגיטלית:</strong>
            <p id="fingerprint_info"></p>
        </div>

        <div class="card">
            <strong>מידע על העוגיות:</strong>
            <p id="cookie_info"></p>
        </div>

        <script>
            // Get user agent
            let userAgent = navigator.userAgent;
            document.getElementById('user_agent').innerHTML = userAgent;

            // Get battery info if supported
            let batteryInfo = "מידע על הסוללה לא זמין";
            if ('getBattery' in navigator) {{
                navigator.getBattery().then(function(battery) {{
                    batteryInfo = "רמת הסוללה: " + (battery.level * 100) + "%, בטעינה: " + (battery.charging ? "כן" : "לא");
                    document.getElementById('battery_info').innerHTML = batteryInfo;
                }});
            }}

            // Get network info
            let networkInfo = "מידע על הרשת לא זמין";
            if ('connection' in navigator) {{
                let connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
                networkInfo = "סוג רשת: " + connection.effectiveType + 
                              ", קצב הורדה: " + connection.downlink + " Mbps, " + 
                              "זמן תגובה: " + connection.rtt + " ms";
                document.getElementById('network_info').innerHTML = networkInfo;
            }}

            // Get screen info
            let screenInfo = window.screen.width + "x" + window.screen.height + ", " + window.screen.colorDepth + " סיביות";
            document.getElementById('screen_info').innerHTML = screenInfo;

            // Combine data for fingerprinting
            function generateFingerprint() {{
                return userAgent + ", " + batteryInfo + ", " + networkInfo + ", " + screenInfo;
            }}

            // Simulate fingerprinting by combining all collected data
            let fingerprint = generateFingerprint();
            document.getElementById('fingerprint_info').innerHTML = "השילוב של המידע הזה יכול לשמש לזיהוי ייחודי של המכשיר שלך: " + fingerprint;

            // Set a first-party cookie (simulating tracking behavior)
            document.cookie = "trackingID=123456; SameSite=None; Secure";
            document.getElementById('cookie_info').innerHTML = "הוגדרה עוגיה: " + document.cookie;

            // Hide loading message after info is loaded
            document.getElementById('loading_message').style.display = "none";
        </script>
    </body>
    </html>
    """, height=800)
