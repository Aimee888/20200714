#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
"""=================================================
@Project -> File    : 20200714 -> test_wifi.py
@IDE     : PyCharm
@Author  : Aimee
@Date    : 2020/7/28 8:41
@Desc    :
================================================="""
import os
import time
import configparser
import pywifi
import wmi
import sys


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class WifiFunc:
    def __init__(self, wifi_name):
        self.name = wifi_name

    def wf_on(self):
        cmd = 'netsh interface set interface "{}" enabled'.format(self.name)
        os.popen(cmd)

    def wf_off(self):
        cmd = 'netsh interface set interface "{}" disabled'.format(self.name)
        os.popen(cmd)

    def get_wf_status(self):
        cmd = 'netsh interface show interface "{}" | find /i ": Enabled"'.format(self.name)
        f = os.popen(cmd)
        data = f.readlines()
        if bool(data):
            wf_status = True
            print("wifi status is on")
        else:
            wf_status = False
            print("wifi status is off")
        f.close()
        return wf_status

    def wf_check_driver(self, wlan_driver_name):
        result_data = 0
        w = wmi.WMI()
        driver_realtek_exist = False
        for drivers in w.Win32_PnPEntity():
            if drivers.name == wlan_driver_name:
                driver_realtek_exist = True
                if drivers.ConfigManagerErrorCode == 0 and drivers.Status == 'OK':
                    print("Driver is OK")
                else:
                    result_data = 1
                    print("Driver is ERROR")
                break
        if not driver_realtek_exist:
            result_data = 1
            print("Not found wlan driver")
        return result_data

    def wf_scan(self):
        result_data = 0
        wifi_obj = pywifi.PyWiFi()
        iface = wifi_obj.interfaces()[0]
        # iface.name()
        # 起始获得的是列表，列表中存放的是无线网卡对象。
        # 可能一台电脑有多个网卡，请注意选择
        # 如果网卡选择错了，程序会卡住，不出结果
        iface.scan()
        time.sleep(3)  # 必须加
        wifi_result = iface.scan_results()
        for i in range(len(wifi_result)):
            # ssid 是名称 ，bssid 是mac地址
            print(wifi_result[i].ssid, wifi_result[i].bssid, wifi_result[i].signal)
        if len(wifi_result) < 1:
            result_data = 1
        return result_data

    def wf_strength(self, ssid_name, max_value, min_value):
        result_data = 0
        wifi_obj = pywifi.PyWiFi()
        iface = wifi_obj.interfaces()[0]
        # iface.name()
        # 起始获得的是列表，列表中存放的是无线网卡对象。
        # 可能一台电脑有多个网卡，请注意选择
        # 如果网卡选择错了，程序会卡住，不出结果
        iface.scan()
        time.sleep(5)  # 必须加
        wifi_result = iface.scan_results()
        for i in range(len(wifi_result)):
            # ssid 是名称 ，bssid 是mac地址
            if wifi_result[i].ssid == ssid_name:
                s = wifi_result[i].signal
                print("Signal is : ", end="")
                print(s)
                if s not in range(min_value, max_value + 1):
                    result_data = 1
                break
        return result_data


def get_value_ini(path_ini, sec_ini, key_ini):
    conf = MyConfigParser()
    conf.read(path_ini)
    value = conf.get(sec_ini, key_ini)
    return value


def help_doc():
    print("Welcome to help document!")
    print("===============================================================")
    print("************** test_wifi Tool V0.1 for Wlan *******************")
    print("Usage:")
    print("test_wifi.exe [parameter1]  [parameter2]")
    print("exp: test_wifi.exe -subtest=wf_on  -inipath=./wifitest.ini")
    print("-subtest: wf_on                 -- start to open wifi")
    print("          wf_off                -- start to close wifi")
    print("          wf_ckdrv              -- Check wlan driver is OK")
    print("          wf_scan               -- Scan nearby wifi")
    print("          wf_strength           -- Check wifi strength in [min, max]")
    print("-inipath: wlan setting file path")
    print("===============================================================")


def main():
    result_data = 0
    argv_dic = {}
    if len(sys.argv) > 1:
        for param in sys.argv[1:]:
            param_list = param.split("=")
            if len(param_list) > 1:
                argv_dic[param_list[0]] = param_list[1]
    else:
        help_doc()
        return result_data
    if argv_dic == {}:
        help_doc()
        result_data = 1
    else:
        try:
            param_item = argv_dic["-subtest"]
        except:
            param_item = None
            s = sys.exc_info()
            str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
            print(str_error)
        if param_item == "wf_on":
            try:
                ini_path = argv_dic["-inipath"]
            except:
                result_data = 1
                ini_path = None
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            try:
                wlanname = get_value_ini(ini_path, "WIFI", "wlanname")
            except:
                result_data = 1
                wlanname = None
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            wf = WifiFunc(wlanname)
            wf.wf_on()
            time.sleep(3)
            status_ok = wf.get_wf_status()
            if not status_ok:
                result_data = 1
        elif param_item == "wf_off":
            try:
                ini_path = argv_dic["-inipath"]
            except:
                result_data = 1
                ini_path = None
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            try:
                wlanname = get_value_ini(ini_path, "WIFI", "wlanname")
            except:
                result_data = 1
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            wf = WifiFunc(wlanname)
            wf.wf_off()
            time.sleep(3)
            status_ok = wf.get_wf_status()
            if status_ok:
                result_data = 1
        elif param_item == "wf_scan":
            wf = WifiFunc("Wi-Fi 3")
            result_data = wf.wf_scan()
        elif param_item == "wf_ckdrv":
            try:
                ini_path = argv_dic["-inipath"]
            except:
                result_data = 1
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            try:
                wlanname = get_value_ini(ini_path, "WIFI", "wlanname")
            except:
                result_data = 1
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            wf = WifiFunc(wlanname)
            try:
                drivername = get_value_ini(ini_path, "WIFI", "drivername")
            except:
                result_data = 1
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            result_data = wf.wf_check_driver(drivername)
        elif param_item == "wf_strength":
            try:
                ini_path = argv_dic["-inipath"]
            except:
                result_data = 1
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            try:
                wlanname = get_value_ini(ini_path, "WIFI", "wlanname")
            except:
                result_data = 1
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            wf = WifiFunc(wlanname)
            try:
                wifiname = get_value_ini(ini_path, "WIFI", "wifiname")
            except:
                result_data = 1
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            try:
                max_str = get_value_ini(ini_path, "WIFI", "max")
                max_int = int(max_str)
                print("max value is: ", end="")
                print(max_int)
            except:
                result_data = 1
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            try:
                min_str = get_value_ini(ini_path, "WIFI", "min")
                min_int = int(min_str)
                print("min value is: ", end="")
                print(min_int)
            except:
                result_data = 1
                s = sys.exc_info()
                str_error = "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
                print(str_error)
                return result_data
            result_data = wf.wf_strength(wifiname, max_int, min_int)
        else:
            result_data = 1
            print("Please check param")
    return result_data


if __name__ == '__main__':
    result = main()
    if result == 0:
        print("pass")
    else:
        print("fail")
    sys.exit(result)
