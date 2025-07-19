import subprocess, json
from constants import DEFAULT_UNKNOWN

def get_bios_version():
    try:
        cmd = ["powershell", "-Command",
               "Get-WmiObject -Class Win32_BIOS | "
               "Select SMBIOSBIOSVersion, Manufacturer, Version, ReleaseDate | ConvertTo-Json"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        bios_info = json.loads(result.stdout)
        if isinstance(bios_info, dict):
            bios_info = [bios_info]
        return [{
            "smbiosBiosVersion": b.get("SMBIOSBIOSVersion", DEFAULT_UNKNOWN),
            "manufacturer": b.get("Manufacturer", DEFAULT_UNKNOWN),
            "version": b.get("Version", DEFAULT_UNKNOWN),
            "releaseDate": b.get("ReleaseDate", DEFAULT_UNKNOWN)
        } for b in bios_info]
    except:
        return []
