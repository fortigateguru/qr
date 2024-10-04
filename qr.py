import streamlit as st
import qrcode
from PIL import Image

# Step 1: Generate QR Code
url = "https://qrcodeinfo.streamlit.app/"  # Replace this with your actual page URL
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

# Step 3: Use JavaScript to pull and display device info
st.write("""
    <script>
        async function getDeviceInfo() {
            let deviceInfo = {};

            // Get user agent
            deviceInfo.userAgent = navigator.userAgent;

            // Get battery info if available
            if (navigator.getBattery) {
                let battery = await navigator.getBattery();
                deviceInfo.battery = {
                    level: (battery.level * 100) + "%",
                    charging: battery.charging ? "Yes" : "No"
                };
            }

            // Display the info inside the Streamlit page
            const displayInfo = `
                <h3>Device Information</h3>
                <p><strong>User Agent:</strong> ${deviceInfo.userAgent}</p>
                <p><strong>Battery Level:</strong> ${deviceInfo.battery ? deviceInfo.battery.level : "Not available"}</p>
                <p><strong>Charging:</strong> ${deviceInfo.battery ? deviceInfo.battery.charging : "Not available"}</p>
            `;
            document.getElementById("device_info").innerHTML = displayInfo;
        }

        // Call the function on page load
        window.onload = function() {
            getDeviceInfo();
        };
    </script>

    <!-- Placeholder where the device info will be shown -->
    <div id="device_info">
        <h3>Loading device info...</h3>
    </div>
""", unsafe_allow_html=True)
