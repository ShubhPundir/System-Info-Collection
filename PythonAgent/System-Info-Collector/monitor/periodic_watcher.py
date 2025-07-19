import time
import hashlib
import json
from system_info.collector import collect_system_info
from api.sender import send_to_api
from .state_manager import load_previous_state, save_current_state
from constants import POLL_INTERVAL

def hash_data(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def start_watching():
    print("Starting hardware configuration watcher...")
    last_state = load_previous_state()
    last_hash = hash_data(last_state)

    while True:
        current_info = collect_system_info()
        current_hash = hash_data(current_info)

        if current_hash != last_hash:
            print("Change detected in system configuration. Sending update...")
            send_to_api(current_info)
            save_current_state(current_info)
            last_hash = current_hash
        else:
            print("No change detected.")

        time.sleep(POLL_INTERVAL)
