import subprocess, json

def get_disk_info():
    try:
        cmd = ["powershell", "-Command", "Get-PhysicalDisk | Select-Object MediaType, Size | ConvertTo-Json"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        disks = json.loads(result.stdout)
        if isinstance(disks, dict):
            disks = [disks]
        ssd_total = sum(d["Size"] for d in disks if "ssd" in d["MediaType"].lower())
        hdd_total = sum(d["Size"] for d in disks if "hdd" in d["MediaType"].lower() or "unspecified" in d["MediaType"].lower())
        return f"{hdd_total // 1_000_000_000} GB", f"{ssd_total // 1_000_000_000} GB"
    except:
        return "0 GB", "0 GB"
