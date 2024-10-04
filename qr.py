import streamlit as st
import qrcode
from PIL import Image
import streamlit.components.v1 as components

# Step 1: Generate QR Code
url = "https://qrcodeinfo.streamlit.app"  # Replace this with your actual page URL
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
        <p id="network_info"></p>
        <p id="screen_info"></p>
        <p id="timezone_info"></p>
        <p id="memory_info"></p>
        <p id="language_info"></p>
        <p id="cpu_info"></p>
        <p id="platform_info"></p>

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

            // Get network info
            if ('connection' in navigator) {
                let connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
                let networkInfo = `Effective Network Type: ${connection.effectiveType}`;
                document.getElementById('network_info').innerHTML = "<strong>Network Info: </strong>" + networkInfo;
            }

            // Get screen info
            let screenWidth = window.screen.width;
            let screenHeight = window.screen.height;
            let colorDepth = window.screen.colorDepth;
            document.getElementById('screen_info').innerHTML = `
                <strong>Screen Width: </strong> ${screenWidth}px <br>
                <strong>Screen Height: </strong> ${screenHeight}px <br>
                <strong>Color Depth: </strong> ${colorDepth} bits
            `;

            // Get time zone
            let timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            document.getElementById('timezone_info').innerHTML = "<strong>Time Zone: </strong>" + timeZone;

            // Get device memory
            if ('deviceMemory' in navigator) {
                let memory = navigator.deviceMemory + " GB";
                document.getElementById('memory_info').innerHTML = "<strong>Device Memory: </strong>" + memory;
            }

            // Get language
            let language = navigator.language || navigator.userLanguage;
            document.getElementById('language_info').innerHTML = "<strong>Language: </strong>" + language;

            // Get hardware concurrency (CPU cores)
            let cpuCores = navigator.hardwareConcurrency;
            document.getElementById('cpu_info').innerHTML = "<strong>CPU Cores: </strong>" + cpuCores;

            // Get platform
            let platform = navigator.platform;
            document.getElementById('platform_info').innerHTML = "<strong>Platform: </strong>" + platform;
        </script>
    </body>
    </html>
    """, height=600)
