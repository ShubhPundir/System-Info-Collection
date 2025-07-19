import hashlib
import json
from system_info.collector import collect_system_info
from api.sender import send_to_api
from monitor.state_manager import load_previous_state, save_current_state
from constants import DEFAULT_UNKNOWN

def hash_data(data):
    """Generate SHA-256 hash of the config dict for comparison"""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def run_startup_check():
    print("Running startup configuration check...")
    last_state = load_previous_state()
    last_hash = hash_data(last_state)

    current_info = collect_system_info()
    current_hash = hash_data(current_info)

    if current_hash != last_hash:
        print(f'{current_hash} != {last_hash}')
        print("Change detected in system configuration. Sending update...")
        # send_to_api(current_info)
        save_current_state(current_info)
    else:
        print("No change detected. Exiting.")
