# Prepare the full Python equivalent of the Java SystemInfoCollector
 
import platform
import psutil
import uuid
import socket
import subprocess
import wmi
import ctypes
import requests
import json
import os
import sys
import re
 
 
DEFAULT_UNKNOWN = "DEFAULT_UNKNOWN"
API_URL = "https://portal.vareli.co.in/asset/api/system-info"
# API_URL = "http://192.168.1.30:8081/asset-management/api/system-info"
# API_URL = "http://192.168.13.28:8080/asset/api/system-info"
 
def get_uuid():
    try:
        # PowerShell command to get the system's UUID
        ps_command = """
        $uuid = (Get-CimInstance -ClassName Win32_ComputerSystemProduct).UUID
        Write-Output $uuid
        """
        # Execute PowerShell command
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            check=True
        )
        # Return the UUID from the output
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
 
def get_device_name():
    try:
        c = wmi.WMI()
        name = c.Win32_ComputerSystem()[0].Name
        return name.strip() if name else DEFAULT_UNKNOWN
    except Exception:
        return DEFAULT_UNKNOWN
 
 
def get_mac_address():
    for iface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == psutil.AF_LINK and snic.address != '00:00:00:00:00:00':
                return snic.address
    return DEFAULT_UNKNOWN
 
 
def get_best_mac_address():
    try:
        c = wmi.WMI()
        ethernet_mac = None
        wifi_mac = None
        for nic in c.Win32_NetworkAdapterConfiguration():
            if not nic.MACAddress or nic.MACAddress == '00:00:00:00:00:00':
                continue
            desc = nic.Description.lower()
            if 'ethernet' in desc and not re.search(r'wireless|wifi|wlan|virtual|bluetooth|loopback|vpn|hamachi', desc):
                ethernet_mac = nic.MACAddress
                break  # Prefer Ethernet
            elif re.search(r'wifi|wireless|wlan', desc):
                wifi_mac = wifi_mac or nic.MACAddress
        return ethernet_mac or wifi_mac or "UNKNOWN"
    except Exception:
        return "UNKNOWN"
 
 
 
def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
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
 
 
def get_chassis_type():
    try:
        cmd = ['powershell', '-Command',
               "Get-WmiObject -Class Win32_SystemEnclosure | Select-Object -ExpandProperty ChassisTypes"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        code = result.stdout.strip().split()[0]
 
        # Group codes into broad categories
        desktop_codes = {"3", "4", "5", "6", "7", "15", "16", "23", "24"}
        laptop_codes = {"8", "9", "10", "14", "30", "31", "32"}
        aio_codes     = {"13"}
 
        if code in desktop_codes:
            return "DESKTOP"
        elif code in laptop_codes:
            return "LAPTOP"
        elif code in aio_codes:
            return "ALL-IN-ONE"
        else:
            return DEFAULT_UNKNOWN
 
    except Exception:
        return DEFAULT_UNKNOWN
 
 
 
def get_processor_info():
    try:
        c = wmi.WMI()
        processor = c.Win32_Processor()[0]
        return processor.Name.strip()
    except:
        return DEFAULT_UNKNOWN
 
 
def get_os_info():
    try:
        system = platform.system()
        release = platform.release()
        version = platform.version()  # contains the build number
        return f"{system} {release} (Build {version})"
    except:
        return "Unknown OS"
 
 
def get_ram_info():
    try:
        # PowerShell command to get total and free physical memory as integers
        ps_command = """
        $total = [math]::Floor((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1MB)
        $free = [math]::Floor((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1KB)
        Write-Output "$total MB"
        Write-Output "$free MB"
        """
        # Execute PowerShell command
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            check=True
        )
        # Split output into total and free memory
        output = result.stdout.strip().split('\n')
        total_mb = output[0].strip()
        free_mb = output[1].strip()
        return total_mb, free_mb
    except subprocess.CalledProcessError as e:
        return "0 MB", "0 MB"
 
 
def get_disk_info():
    try:
        cmd = [
            "powershell",
            "-Command",
            "Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size | ConvertTo-Json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        disks = json.loads(result.stdout)
       
        if isinstance(disks, dict):
            disks = [disks]
       
        ssd_total = 0
        hdd_total = 0
       
        for disk in disks:
            size = disk.get("Size", 0)
            media_type = disk.get("MediaType", "").lower()
            if "ssd" in media_type:
                ssd_total += size
            elif "hdd" in media_type:
                hdd_total += size
            elif "unspecified" in media_type:
                hdd_total += size
 
        # Manufacturer decimal GB (1 GB = 1,000,000,000 bytes)
        hdd_total_gb = ssd_total_gb = 0
        if hdd_total > 0:
            hdd_total_gb = hdd_total // 1_000_000_000
        if ssd_total > 0:
            ssd_total_gb = ssd_total // 1_000_000_000
 
        return f"{hdd_total_gb} GB", f"{ssd_total_gb} GB"
   
    except Exception as e:
        print("Error:", e)
        return "0 GB", "0 GB"
 
def get_graphics_info():
    try:
        c = wmi.WMI()
        gpu = c.Win32_VideoController()[0]
        raw_ram = gpu.AdapterRAM
        if raw_ram < 0:
            raw_ram = ctypes.c_uint32(raw_ram).value
        ram_mb = raw_ram // (1024 * 1024)
        return gpu.Name.strip(), f"{ram_mb} MB"
    except Exception as e:
        return DEFAULT_UNKNOWN, DEFAULT_UNKNOWN
 
 
def get_antivirus_info():
    try:
        cmd = ['powershell', '-Command',
               "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct | Select-Object -ExpandProperty displayName"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip() or DEFAULT_UNKNOWN
    except:
        return DEFAULT_UNKNOWN
   
   
def get_bios_version():
    try:
        cmd = [
            "powershell",
            "-Command",
            "Get-WmiObject -Class Win32_BIOS | "
            "Select-Object SMBIOSBIOSVersion, Manufacturer, Version, ReleaseDate | "
            "ConvertTo-Json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        bios_info = json.loads(result.stdout)
       
        # Ensure bios_info is always a list
        if isinstance(bios_info, dict):
            bios_info = [bios_info]
 
        bios_list = []
 
        for entry in bios_info:
            bios_list.append({
                "smbiosBiosVersion": entry.get("SMBIOSBIOSVersion", DEFAULT_UNKNOWN),
                "manufacturer": entry.get("Manufacturer", DEFAULT_UNKNOWN),
                "version": entry.get("Version", DEFAULT_UNKNOWN),
                "releaseDate": entry.get("ReleaseDate", DEFAULT_UNKNOWN)
            })
 
        return bios_list
 
    except Exception as e:
        print("Error:", e)
        return []
 
 
   
def get_installed_software(third_party_only=True):
    try:
        filter_condition = "Where-Object { $_.DisplayName -ne $null"
        if third_party_only:
            filter_condition += " -and $_.Publisher -notlike '*Microsoft*' -and $_.SystemComponent -ne $true"
        filter_condition += " }"
 
        cmd = [
            "powershell", "-Command",
            f"Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*, "
            f"HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | "
            f"{filter_condition} | "
            "Select-Object DisplayName, DisplayVersion, Publisher | "
            "ConvertTo-Json -Compress"
        ]
 
        result = subprocess.run(cmd, capture_output=True, text=True)
 
        if result.returncode != 0 or not result.stdout.strip():
            return []
 
        software_entries = json.loads(result.stdout)
 
        # Ensure it's a list
        if isinstance(software_entries, dict):
            software_entries = [software_entries]
 
        installed = []
        for entry in software_entries:
            installed.append({
                "name": entry.get("DisplayName", DEFAULT_UNKNOWN),
                "version": entry.get("DisplayVersion", DEFAULT_UNKNOWN),
                "publisher": entry.get("Publisher", DEFAULT_UNKNOWN)
            })
 
        return installed
 
    except Exception as e:
        return []
   
 
def get_company_info_from_filename():
    try:
        filename = os.path.basename(sys.argv[0])  # Gets the script name (e.g., TRFCHKND85(1).exe)
        base_name = os.path.splitext(filename)[0]  # Remove .exe -> TRFCHKND85(1)
 
        # Remove trailing copy patterns
        cleaned_name = re.sub(r"(?:\s*-\s*Copy(?:\s*\(.*\))?|\s*\(.*\)|_\d+)$", "", base_name, flags=re.IGNORECASE)
 
        company_code = cleaned_name.strip()
 
        return company_code
    except Exception as e:
        print(f"Error extracting company info from filename: {e}")
        sys.exit(1)
 
 
def collect_system_info():
    serial_number, manufacturer, model = get_serial_number_and_model()
    dto = {
        "companyCode": get_company_info_from_filename(),
        "deviceName": get_device_name(),
        "assetType": get_chassis_type(),
        "uuid": get_uuid(),
        "macAddress": get_mac_address(),
        "processor": get_processor_info(),
        "os": get_os_info(),
        "ram": get_ram_info()[0],
        "availableRam": get_ram_info()[0],
        "hddTotal": get_disk_info()[0],
        "ssdTotal": get_disk_info()[1],
        "serialNumber": serial_number,
        "manufacturer": manufacturer,
        "model": model,
        "graphicsCard": get_graphics_info()[0],
        "graphicsCardVRam": get_graphics_info()[1],
        "antiVirus": get_antivirus_info(),
        "ipAddress": get_ip_address(),
        "installedSoftware": get_installed_software(),
        "bios": get_bios_version()
    }
    return dto
 
 
def send_to_api(data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(API_URL, headers=headers, data=json.dumps(data), timeout=5)
       

        if response.status_code == 200:
            # Success: exit immediately
            sys.exit(0)
        else:
            # Non-200: print and wait
            print(f"Unexpected response ({response.status_code}):")
            print(response.text)
            input("Press Enter to exit...")
 
    except Exception as e:
        print("Failed to send system info:", e)
        input("Press Enter to exit...")
 
 
 
if __name__ == "__main__":
    info = collect_system_info()
    print(info)
    # send_to_api(info)
 
 
 