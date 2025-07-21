from .identity import get_uuid, get_device_name, get_serial_number_and_model
from .network import get_mac_address, get_ip_address
from .os_info import get_os_info
from .cpu import get_processor_info
from .memory import get_ram_info
from .disk import get_disk_info
from .graphics import get_graphics_info
from .chassis import get_chassis_type
from .antivirus import get_antivirus_info
from .bios import get_bios_version
from .software import get_installed_software
from .utils import get_company_info_from_filename

def collect_system_info():
    serial_number, manufacturer, model = get_serial_number_and_model()
    ram_total, ram_free = get_ram_info()
    hdd, ssd = get_disk_info()
    gpu, vram = get_graphics_info()

    return {
        "companyCode": get_company_info_from_filename(),
        "deviceName": get_device_name(),
        "assetType": get_chassis_type(),
        "uuid": get_uuid(),
        "macAddress": get_mac_address(),
        "processor": get_processor_info(),
        "os": get_os_info(),
        "ram": ram_total,
        # "availableRam": ram_free,
        "hddTotal": hdd,
        "ssdTotal": ssd,
        "serialNumber": serial_number,
        "manufacturer": manufacturer,
        "model": model,
        "graphicsCard": gpu,
        "graphicsCardVRam": vram,
        "antiVirus": get_antivirus_info(),
        "ipAddress": get_ip_address(),
        "installedSoftware": get_installed_software(),
        "bios": get_bios_version()
    }
