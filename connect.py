import subprocess

# Define Wi-Fi credentials
WIFI_SSID = "ManagementAP"   # Change to your network name
WIFI_PASS = ""  # Change to your network password

def get_wifi_name():
    try:
        # Run iwgetid to get the SSID
        result = subprocess.run(["iwgetid", "-r"], capture_output=True, text=True, check=True)
        wifi_name = result.stdout.strip()

        if wifi_name:
            return wifi_name
        else:
            return "Not connected to Wi-Fi"

    except subprocess.CalledProcessError:
        return "Error: Unable to retrieve Wi-Fi name"


def connect_to_wifi(ssid, password):
    try:
        # Check if the Wi-Fi network exists
        scan_result = subprocess.run(["nmcli", "-t", "-f", "SSID", "dev", "wifi"], capture_output=True, text=True)
        if ssid not in scan_result.stdout:
            print(f"⚠ Wi-Fi network '{ssid}' not found! Make sure it is available.")
            return False

        # Connect to the Wi-Fi network
        subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password], check=True)
        print(f"✅ Successfully connected to {ssid}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to connect to {ssid}: {e}")
        return False

