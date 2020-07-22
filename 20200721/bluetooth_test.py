#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
"""=================================================
@Project -> File    : 20200714 -> bluetooth.py
@IDE     : PyCharm
@Author  : Aimee
@Date    : 2020/7/21 11:03
@Desc    :
================================================="""
from bluetooth import *


def findDevs():
    already_found = []
    print("start searching...")
    found_devs = discover_devices(duration=30, lookup_names=True)
    for (addr, name) in found_devs:
        if addr not in already_found:
            print("[*]Found Bluetooth Device : " + str(name))
            print("[+] MAC address: " + str(addr))
            print("")
            already_found.append(addr)


def auto_discovery():
    # Return address once the first openxc device found
    try:
        nearby_devices = discover_devices(lookup_names=True)
        print("found device: ", len(nearby_devices))
    except BluetoothError as e:
        print("BT error %s" % e)
        return None

    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))

    discovery_once = True
    return discovery_once


if __name__ == '__main__':
    # findDevs()
    auto_discovery()
