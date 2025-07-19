import requests, json, sys
from constants import API_URL

def send_to_api(data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(API_URL, headers=headers, data=json.dumps(data), timeout=5)
        if response.status_code == 200:
            sys.exit(0)
        else:
            print(f"Unexpected response ({response.status_code}):\n{response.text}")
            input("Press Enter to exit...")
    except Exception as e:
        print("Failed to send system info:", e)
        input("Press Enter to exit...")
