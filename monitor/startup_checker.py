import json
from system_info.collector import collect_system_info
from api.sender import send_to_api
from monitor.state_manager import load_previous_state, save_current_state
from .hash import hash_data

def print_diff(old, new):
    print("####"*20)
    print("PRINTING THE DIFFERENCE IN CONFIGURATION")
    print("####"*20)
    for k in new:
        if old.get(k) != new[k]:
            print(f"- {k}: {old.get(k)} → {new[k]}")

def run_startup_check():
    print("Running startup configuration check...")
    last_state = load_previous_state()
    last_hash = hash_data(last_state)

    current_info = collect_system_info()
    current_hash = hash_data(current_info)

    if current_hash != last_hash:
        print("Change detected in system configuration. Sending update...")
        # print_diff(last_state, current_info)
        # send_to_api(current_info)
        save_current_state(current_info)
    else:
        print("No change detected. Exiting Full Check.")
