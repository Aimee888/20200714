#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
"""=================================================
@Project -> File    : 20200714 -> BT_test.py
@IDE     : PyCharm
@Author  : Aimee
@Date    : 2020/7/23 8:13
@Desc    :
目前问题：
    1. 扫描附近蓝牙时，如果之前有配对成功过的蓝牙，哪怕现在没有开启蓝牙，也可以扫描到
    2. 如果没有powershell.exe，会红屏报错，但是bt_on和bt_off返回值还是0，因为批处理没有错误的返回值，现在想找办法
        监测现在蓝牙状态是on还是off，就可以解决返回值的问题
================================================="""
import subprocess
import wmi
from bluetooth import *
import sys
import configparser


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


def get_value_ini(path_ini, sec_ini, key_ini):
    conf = MyConfigParser()
    conf.read(path_ini)
    value = conf.get(sec_ini, key_ini)
    return value


# 帮助文档
def help_doc():
    print("Welcome to help document!")
    print("===============================================================")
    print("************** BT_test Tool V0.1 for Bluetooth ****************")
    print("Usage:")
    print("BT_test.exe [parameter1]")
    print("exp: BT_test.exe -subtest=bt_on")
    print("-subtest: bt_on                 -- start to open bluetooth")
    print("          bt_off                -- start to close bluetooth")
    print("          bt_check_driver       -- Check bluetooth driver is OK")
    print("          bt_scan_nearby_device -- Scan nearby bluetooth device")
    print("")
    print("BT_test.exe [parameter1] [parameter2]")
    print("function1: Check certain bluetooth device mac")
    print("exp: BT_test.exe -subtest=bt_check_certain_device_by_name -inipath=bt_test.ini")
    print("    -subtest: [bt_check_certain_device_by_name]")
    print("    -inipath: bluetooth setting file path")
    print("===============================================================")


# 关闭蓝牙
def bt_off():
    result_data = 0
    cmd_off = "Powershell.exe -executionpolicy remotesigned -command .\Bluetooth.ps1  -BluetoothStatus Off"
    # cmd_off = "Powershell.exe -executionpolicy Restricted -command .\Bluetooth.ps1  -BluetoothStatus Off"
    # cmd_off = "Powershell.exe -executionpolicy AllSigned -command .\Bluetooth.ps1  -BluetoothStatus Off"
    # cmd_off = "Powershell.exe -executionpolicy Unrestricted -command .\Bluetooth.ps1  -BluetoothStatus Off"
    try:
        subprocess.Popen(cmd_off, shell=True)
        print("Bluetooth status is Off!")
    except:
        result_data = 1
        s = sys.exc_info()
        str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
        print(str_error)
        print("Close bluetooth failed")
    return result_data


# 开启蓝牙
def bt_on():
    result_data = 0
    cmd_on = "Powershell.exe -executionpolicy remotesigned -command .\Bluetooth.ps1  -BluetoothStatus On"
    try:
        subprocess.Popen(cmd_on, shell=True)
        print("Bluetooth status os On!")
    except:
        result_data = 1
        s = sys.exc_info()
        str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
        print(str_error)
        print("Open bluetooth failed")
    return result_data


# 检查是否存在蓝牙驱动以及驱动是否正常
def bt_check_driver():
    result_data = 0
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
                    result_data = 1
                    print("Driver is ERROR")
    if not driver_bluetooth_exist:
        result_data = 1
        print("Not found bluetooth driver")
    return result_data


# 扫描附近蓝牙设备
def bt_scan_nearby_device():
    result_data = 0
    try:
        nearby_devices = discover_devices(lookup_names=True)
        print("found device: ", len(nearby_devices))
        device_number = len(nearby_devices)
        if device_number == 0:
            result_data = 1
    except BluetoothError as e:
        print("BT error %s" % e)
        result_data = 1
        return result_data

    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))
    return result_data


# 检查特定蓝牙设备的mac地址
def check_certain_device_by_name(device_name):
    result_data = 0
    target_name = device_name
    target_address = None

    nearby_devices = discover_devices(duration=30, lookup_names=True)
    for addr, name in nearby_devices:
        if target_name == name:
            target_address = addr
            break
    if target_address is not None:
        print("found {} device with address {}".format(target_name, target_address))
    else:
        result_data = 1
        print("could not find {} device nearby".format(target_name))
    return result_data


def bt_check_certain_device_by_name(argv_dic, param_item):
    result_data = 0
    try:
        ini_path = argv_dic["-inipath"]
    except:
        result_data = 1
        ini_path = None
        s = sys.exc_info()
        str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
        print(str_error)
    try:
        device_name = get_value_ini(ini_path, param_item, "device_name")
    except:
        result_data = 1
        device_name = None
        s = sys.exc_info()
        str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
        print(str_error)
    if device_name is not None:
        result_data = check_certain_device_by_name(device_name)
    return result_data


def main():
    result_data = 0
    argv_dic = {}
    for param in sys.argv[1:]:
        param_list = param.split("=")
        if len(param_list) > 1:
            argv_dic[param_list[0]] = param_list[1]
    if argv_dic == {}:
        help_doc()
    else:
        try:
            param_item = argv_dic["-subtest"]
        except:
            param_item = None
            s = sys.exc_info()
            str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
            print(str_error)
        if param_item == "bt_on":
            result_data = bt_on()
        elif param_item == "bt_off":
            result_data = bt_off()
        elif param_item == "bt_check_driver":
            result_data = bt_check_driver()
        elif param_item == "bt_scan_nearby_device":
            result_data = bt_scan_nearby_device()
        elif param_item == "bt_check_certain_device_by_name":
            result_data = bt_check_certain_device_by_name(argv_dic, param_item)
        else:
            result_data = 1
            print("Please check parameter is OK?")
    return result_data


if __name__ == '__main__':
    result = main()
    sys.exit(result)
