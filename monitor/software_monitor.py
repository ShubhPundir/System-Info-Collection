# monitor/real_time_install_monitor.py
import win32con, win32api, win32event
import winreg
import threading
import time
from api.sender import send_to_api

REG_NOTIFY_CHANGE_NAME = 0x00000001

watch_keys = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
]

def read_subkey_details(root, path, subkey_name):
    try:
        with winreg.OpenKey(root, f"{path}\\{subkey_name}") as key:
            name = winreg.QueryValueEx(key, "DisplayName")[0]
            version = winreg.QueryValueEx(key, "DisplayVersion")[0] if "DisplayVersion" in [winreg.EnumValue(key, i)[0] for i in range(winreg.QueryInfoKey(key)[1])] else None
            publisher = winreg.QueryValueEx(key, "Publisher")[0] if "Publisher" in [winreg.EnumValue(key, i)[0] for i in range(winreg.QueryInfoKey(key)[1])] else None
            return {
                "name": name,
                "version": version or "UNKNOWN",
                "publisher": publisher or "UNKNOWN",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception:
        return None

def watch_single_registry_key(root, path):
    with winreg.OpenKey(root, path, 0, winreg.KEY_READ | winreg.KEY_NOTIFY) as key:
        subkeys_before = set()
        try:
            i = 0
            while True:
                subkey = winreg.EnumKey(key, i)
                subkeys_before.add(subkey)
                i += 1
        except OSError:
            pass

        while True:
            win32api.RegNotifyChangeKeyValue(key, True, REG_NOTIFY_CHANGE_NAME, None, False)
            time.sleep(1)  # Let registry settle
            subkeys_after = set()
            try:
                i = 0
                while True:
                    subkey = winreg.EnumKey(key, i)
                    subkeys_after.add(subkey)
                    i += 1
            except OSError:
                pass

            new_keys = subkeys_after - subkeys_before
            subkeys_before = subkeys_after

            for new_subkey in new_keys:
                details = read_subkey_details(root, path, new_subkey)
                if details and details["name"]:
                    print("[Detected Install]", details)
                    # send_to_api({
                    #     **details,
                    #     "event": "installed"
                    # })
                    # TODO
                    # 1. Add local ledger/json update script
                    # 2. Refactor sent_to_api
                    # 3. Add functionality to factor uninstall changes as well


def start_real_time_install_monitor():
    for root, path in watch_keys:
        threading.Thread(
            target=watch_single_registry_key,
            args=(root, path),
            daemon=True
        ).start()
