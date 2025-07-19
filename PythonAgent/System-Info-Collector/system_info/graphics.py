import wmi, ctypes
from constants import DEFAULT_UNKNOWN

def get_graphics_info():
    try:
        c = wmi.WMI()
        gpu = c.Win32_VideoController()[0]
        ram = gpu.AdapterRAM if gpu.AdapterRAM >= 0 else ctypes.c_uint32(gpu.AdapterRAM).value
        return gpu.Name.strip(), f"{ram // (1024 * 1024)} MB"
    except:
        return DEFAULT_UNKNOWN, DEFAULT_UNKNOWN
