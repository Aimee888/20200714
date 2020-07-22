#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
"""=================================================
@Project -> File    : 20200714 -> BT_off.py
@IDE     : PyCharm
@Author  : Aimee
@Date    : 2020/7/22 17:08
@Desc    :
================================================="""
import subprocess


def main():
    privage_pow = ".\powershell.exe Set-ExecutionPolicy Unrestricted"
    subprocess.Popen(privage_pow, shell=True)
    cmd_on = ".\powershell.exe -command .\Bluetooth.ps1 -BluetoothStatus Off"
    subprocess.Popen(cmd_on, shell=True)
    print("Bluetooth status os Off!")


if __name__ == '__main__':
    main()
