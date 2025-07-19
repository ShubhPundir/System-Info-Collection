import json
import os
from constants import STATE_FILE

def load_previous_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_current_state(current_info):
    with open(STATE_FILE, 'w') as f:
        json.dump(current_info, f, indent=2)
