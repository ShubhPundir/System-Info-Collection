import subprocess

def get_ram_info():
    try:
        ps_command = """
        $total = [math]::Floor((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1MB)
        $free = [math]::Floor((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1KB)
        Write-Output "$total MB`n$free MB"
        """
        result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True, check=True)
        total_mb, free_mb = result.stdout.strip().split('\n')
        return total_mb, free_mb
    except:
        return "0 MB", "0 MB"
