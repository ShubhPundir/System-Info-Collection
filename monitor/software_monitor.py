# monitor/real_time_install_monitor.py
import win32con, win32api, win32event
import winreg
import threading
import time
from constants import DEFAULT_UNKNOWN
from api.sender import send_to_api

REG_NOTIFY_CHANGE_NAME = 0x00000001

watch_keys = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
]

def get_current_subkeys(root, path):
    subkeys = set()
    try:
        with winreg.OpenKey(root, path) as key:
            i = 0
            while True:
                try:
                    subkey = winreg.EnumKey(key, i)
                    subkeys.add(subkey)
                    i += 1
                except OSError:
                    break # Means we have reached the end of the list of registry subkeys
    except FileNotFoundError:
        print("Registry path does not exist")
    return subkeys

def read_subkey_details(root, path, subkey_name):
    try:
        with winreg.OpenKey(root, f"{path}\\{subkey_name}") as key:
            name = winreg.QueryValueEx(key, "DisplayName")[0]
            values = {winreg.EnumValue(key, i)[0]: winreg.EnumValue(key, i)[1] for i in range(winreg.QueryInfoKey(key)[1])}
            return {
                "name": name,
                "version": values.get("DisplayVersion", "UNKNOWN"),
                "publisher": values.get("Publisher", "UNKNOWN"),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception:
        return None

def watch_single_registry_key(root, path):
    with winreg.OpenKey(root, path, 0, winreg.KEY_READ | winreg.KEY_NOTIFY) as key:
        previous_subkeys = get_current_subkeys(root, path)

        while True:
            win32api.RegNotifyChangeKeyValue(key, True, REG_NOTIFY_CHANGE_NAME, None, False)
            time.sleep(1)  # Debounce to avoid race conditions
            current_subkeys = get_current_subkeys(root, path)

            # Detect installs
            new_keys = current_subkeys - previous_subkeys
            for subkey in new_keys:
                details = read_subkey_details(root, path, subkey)
                if details and details["name"]:
                    print("[Detected Install]", details)
                    # send_to_api({**details, "event": "installed"})

            # Detect uninstalls
            removed_keys = previous_subkeys - current_subkeys
            for subkey in removed_keys:
                print(f"[Detected Uninstall] {subkey}")
                # send_to_api({"name": subkey, "event": "uninstalled", "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')})

            previous_subkeys = current_subkeys


def start_real_time_install_monitor():
    for root, path in watch_keys:
        threading.Thread(
            target=watch_single_registry_key,
            args=(root, path),
            daemon=True
        ).start()