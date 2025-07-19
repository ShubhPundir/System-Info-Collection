import subprocess
from constants import DEFAULT_UNKNOWN

def get_antivirus_info():
    try:
        cmd = ["powershell", "-Command", "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct | Select-Object -ExpandProperty displayName"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip() or DEFAULT_UNKNOWN
    except:
        return DEFAULT_UNKNOWN
