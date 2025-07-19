import subprocess
from constants import DEFAULT_UNKNOWN

def get_chassis_type():
    try:
        cmd = ["powershell", "-Command", "Get-WmiObject -Class Win32_SystemEnclosure | Select-Object -ExpandProperty ChassisTypes"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        code = result.stdout.strip().split()[0]
        if code in {"3", "4", "5", "6", "7", "15", "16", "23", "24"}:
            return "DESKTOP"
        elif code in {"8", "9", "10", "14", "30", "31", "32"}:
            return "LAPTOP"
        elif code == "13":
            return "ALL-IN-ONE"
        return DEFAULT_UNKNOWN
    except:
        return DEFAULT_UNKNOWN
