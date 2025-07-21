from system_info.collector import collect_system_info
from monitor.startup_checker import run_startup_check
from monitor.software_monitor import start_real_time_install_monitor
from constants import STATE_FILE


def main():
    import sys
    import datetime
    print(f"[MAIN START] {datetime.datetime.now()}\n")
    if len(sys.argv) > 1:
        if sys.argv[1] == '--once':
            import json
            print("INITIATING THE COLLECTION OF SYS_INFO")
            info = collect_system_info()
            with open(STATE_FILE, 'w') as f:
                json.dump(info, f, indent=2)
            print(info)
    else:
        run_startup_check()
        start_real_time_install_monitor()
        print(f"[Client Running] to stop Press the off button of your PC. {datetime.datetime.now()}\n")
        while True:
            pass


if __name__ == "__main__":
    main()