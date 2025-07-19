import hashlib
import json
def normalize_for_hashing(data):
    volatile_keys = [
        "availableRam",        # naturally changes
        "ipAddress",           # DHCP / VPN
        "installedSoftware",   # Software changes are ignored
        # TODO
        # might add this to constants.py
    ]
    return {k: v for k, v in data.items() if k not in volatile_keys}

def hash_data(data):
    normalized = normalize_for_hashing(data)
    return hashlib.sha256(json.dumps(normalized, sort_keys=True).encode()).hexdigest()
