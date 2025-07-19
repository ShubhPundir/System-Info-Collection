import os, sys, re

def get_company_info_from_filename():
    try:
        filename = os.path.basename(sys.argv[0])
        # depends on the name of the main.py file
        # TODO
        # Should be entered once when installed and registered as an app
        base_name = os.path.splitext(filename)[0]
        return re.sub(r"(?:\s*-\s*Copy(?:\s*\(.*\))?|\s*\(.*\)|_\d+)$", "", base_name, flags=re.IGNORECASE)
    except:
        sys.exit(1)
