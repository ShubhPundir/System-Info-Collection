import wmi

c = wmi.WMI()
for item in c.query("SELECT * FROM Win32_Product"):
    print(item.Name, item.Version)