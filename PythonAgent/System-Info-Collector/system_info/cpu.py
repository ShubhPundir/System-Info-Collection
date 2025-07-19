import wmi
from constants import DEFAULT_UNKNOWN

def get_processor_info():
    try:
        c = wmi.WMI()
        return c.Win32_Processor()[0].Name.strip()
    except:
        return DEFAULT_UNKNOWN
