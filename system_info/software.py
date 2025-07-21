import subprocess, json
from constants import DEFAULT_UNKNOWN

def get_installed_software(third_party_only=True):
    try:
        filter_condition = "Where-Object { $_.DisplayName -ne $null"
        if third_party_only:
            filter_condition += " -and $_.Publisher -notlike '*Microsoft*' -and $_.SystemComponent -ne $true"
        filter_condition += " }"

        cmd = [
            "powershell", "-Command",
            f"Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*, "
            f"HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | {filter_condition} | "
            f"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | {filter_condition} | "
            "Select DisplayName, DisplayVersion, Publisher | ConvertTo-Json -Compress"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        if isinstance(data, dict):
            data = [data]
        return [{"name": d.get("DisplayName", DEFAULT_UNKNOWN),
                 "version": d.get("DisplayVersion", DEFAULT_UNKNOWN),
                 "publisher": d.get("Publisher", DEFAULT_UNKNOWN)} for d in data]
    except:
        return []
