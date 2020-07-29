#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
"""=================================================
@Project -> File    : six-dialog_design -> download_song.py
@IDE     : PyCharm
@Author  : Aimee
@Date    : 2020/6/2 9:13
@Desc    :参考链接：https://www.cnblogs.com/dcpeng/p/12922969.html
默认需要同级目录的link.ini文件
================================================="""
from WangYY import get_ini_section, wangyiyun_start
from kuwo import kuwo_start


def main():
    ini_path = "./link.ini"
    sections = get_ini_section(ini_path)
    sec_dic = {}
    for num, section in enumerate(sections):
        sec_dic[num+1] = section
        print(str(num + 1) + ". " + section)
    a = input("请选择一个通道：")
    if sec_dic[int(a)] == "网易云":  # 网易云音乐下载
        wangyiyun_start(ini_path, sec_dic[int(a)])
    elif sec_dic[int(a)] == "酷我":  # 酷我音乐下载
        kuwo_start(ini_path, sec_dic[int(a)])


if __name__ == '__main__':
    main()
