#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
"""=================================================
@Project -> File    : 20200714 -> kuwo.py
@IDE     : PyCharm
@Author  : Aimee
@Date    : 2020/7/29 14:26
@Desc    :https://www.cnblogs.com/smart-zihan/p/12745679.html
酷我音乐的网址：http://www.kuwo.cn/
rid的来由：找到自己喜欢的一首歌，点开它，看网址上面最后一串数字就是rid
================================================="""
import configparser
import requests


def get_ini_value(ini_path, section, key):
    conf = configparser.ConfigParser()
    # 如果ini中有中文，就加上encoding
    conf.read(ini_path, encoding="utf-8")
    value = conf.get(section, key)
    return value


def get_ini_section(ini_path):
    conf = configparser.ConfigParser()
    conf.read(ini_path, encoding="utf-8")
    sections = conf.sections()
    return sections


def kuwo_start(ini_path, section):
    rid = get_ini_value(ini_path, section, "rid")
    url = "http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1587429921873&reqId=617f0321-8369-11ea-80b3-bbd056ce88a1".format(rid)
    data = requests.get(url).json()
    song_url = data["url"]
    song_data = requests.get(song_url).content
    song_name = get_ini_value(ini_path, section, "songname")
    song_savepath = "酷我/" + song_name + ".mp3"
    with open(song_savepath, "wb") as f:
        f.write(song_data)
    print(song_name, end="")
    print("\t下载完成")
