import streamlit as st
import qrcode
from PIL import Image
import streamlit.components.v1 as components

# Step 1: Generate QR Code
url = "https://qrcodeinfo.streamlit.app"  # Your website where the JS will run
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Create image of the QR code
img = qr.make_image(fill="black", back_color="white")
img = img.convert("RGB")
img.save("qr_code.png")

# Step 2: Show the QR code in Streamlit app
st.title("Scan the QR Code to Get Device Info")
st.image(img)

# Step 3: Use components.html to run JS and display device info
components.html("""
    <html>
    <body>
        <h3>Device Information</h3>
        <p id="user_agent"></p>
        <p id="battery_info"></p>

        <script>
            // Get user agent
            document.getElementById('user_agent').innerHTML = "<strong>User Agent: </strong>" + navigator.userAgent;

            // Get battery info if supported
            if ('getBattery' in navigator) {
                navigator.getBattery().then(function(battery) {
                    var level = battery.level * 100 + "%";
                    var charging = battery.charging ? "Yes" : "No";
                    document.getElementById('battery_info').innerHTML = "<strong>Battery Level: </strong>" + level + "<br><strong>Charging: </strong>" + charging;
                });
            } else {
                document.getElementById('battery_info').innerHTML = "<strong>Battery info not supported by this browser.</strong>";
            }
        </script>
    </body>
    </html>
    """, height=300)
