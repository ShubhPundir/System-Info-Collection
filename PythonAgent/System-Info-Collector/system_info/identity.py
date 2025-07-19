import wmi
import subprocess
from constants import DEFAULT_UNKNOWN

def get_uuid():
    try:
        ps_command = '(Get-CimInstance -ClassName Win32_ComputerSystemProduct).UUID'
        result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        return DEFAULT_UNKNOWN

def get_device_name():
    try:
        c = wmi.WMI()
        return c.Win32_ComputerSystem()[0].Name.strip()
    except:
        return DEFAULT_UNKNOWN

def get_serial_number_and_model():
    try:
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        system = c.Win32_ComputerSystem()[0]
        return bios.SerialNumber.strip(), system.Manufacturer.strip(), system.Model.strip()
    except:
        return DEFAULT_UNKNOWN, DEFAULT_UNKNOWN, DEFAULT_UNKNOWN
