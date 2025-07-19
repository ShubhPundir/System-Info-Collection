import psutil, wmi, socket, re
from constants import DEFAULT_UNKNOWN

def get_mac_address():
    for iface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == psutil.AF_LINK and snic.address != '00:00:00:00:00:00':
                return snic.address
    return DEFAULT_UNKNOWN

def get_best_mac_address():
    try:
        c = wmi.WMI()
        for nic in c.Win32_NetworkAdapterConfiguration():
            if not nic.MACAddress or nic.MACAddress == '00:00:00:00:00:00':
                continue
            desc = nic.Description.lower()
            if 'ethernet' in desc and not re.search(r'wireless|wifi|wlan|virtual|bluetooth|loopback|vpn|hamachi', desc):
                return nic.MACAddress
        return DEFAULT_UNKNOWN
    except:
        return DEFAULT_UNKNOWN

def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return DEFAULT_UNKNOWN
