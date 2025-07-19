import platform

def get_os_info():
    try:
        system = platform.system()
        release = platform.release()
        version = platform.version()
        return f"{system} {release} (Build {version})"
    except:
        return "Unknown OS"
