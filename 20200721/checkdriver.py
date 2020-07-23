import wmi


if __name__ == '__main__':
    w = wmi.WMI()
    driver_bluetooth_exist = False
    for drivers in w.Win32_PnPEntity():
        if drivers.Name is not None:
            # if (drivers.Name.find("Bluetooth")) != -1:
            if drivers.Name == "Bluetooth":
                driver_bluetooth_exist = True
                if drivers.ConfigManagerErrorCode == 0 and drivers.Status == 'OK':
                    print("Driver is OK")
                else:
                    print("Driver is ERROR")
    if not driver_bluetooth_exist:
        print("Not found bluetooth driver")
