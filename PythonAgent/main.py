from system_info.collector import collect_system_info
from monitor.startup_checker import run_startup_check
from constants import STATE_FILE

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '--startup':
            run_startup_check() 
    else:
        import json
        print("INITIATING THE COLLECTION OF SYS_INFO")
        info = collect_system_info()
        with open(STATE_FILE, 'w') as f:
            json.dump(info, f, indent=2)
        print(info)
        
