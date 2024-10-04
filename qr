import streamlit as st
import qrcode
from PIL import Image

# Step 1: Generate QR Code
url = "https://datacompare.net"  # Your website where the JS will run
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

# Step 3: Embed JS to capture device info
st.write("""
    <script>
        // Get user agent and battery information
        function getDeviceInfo() {
            const deviceInfo = {};
            deviceInfo.userAgent = navigator.userAgent;

            navigator.getBattery().then(function(battery) {
                deviceInfo.battery = {
                    level: battery.level * 100 + "%",
                    charging: battery.charging ? "Yes" : "No"
                };
                // Send the information back to the Streamlit app
                document.getElementById("device_info").innerHTML = `
                    <h3>Device Information</h3>
                    <p>User Agent: ${deviceInfo.userAgent}</p>
                    <p>Battery Level: ${deviceInfo.battery.level}</p>
                    <p>Charging: ${deviceInfo.battery.charging}</p>
                `;
            });
        }

        // Run the function when page loads
        window.onload = function() {
            getDeviceInfo();
        };
    </script>

    <div id="device_info"></div>
""", unsafe_allow_html=True)
