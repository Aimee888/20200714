#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
"""=================================================
@Project -> File    : 20200714 -> wangyiyun_download.py
@IDE     : PyCharm
@Author  : Aimee
@Date    : 2020/7/29 14:22
@Desc    :
================================================="""
import requests
import re
import configparser


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


def wangyiyun_download(ini_path, section, song_id, song_name):
    song_url_part = get_ini_value(ini_path, section, "urlsong")
    song_url = song_url_part.format(song_id)
    print("正在下载歌曲: {}".format(song_name), end='')
    data = requests.get(song_url).content
    song_savepath = "网易云/" + song_name + ".mp3"
    with open(song_savepath, "wb") as f:
        f.write(data)
    print("\t下载完成")


def wangyiyun_start(ini_path, section):
    mainsongid = get_ini_value(ini_path, section, "mainsongid")
    if mainsongid.lower() == "true":
        song_id = get_ini_value(ini_path, section, "songid")
        song_name = get_ini_value(ini_path, section, "songname")
        wangyiyun_download(ini_path, section, song_id, song_name)
    else:
        id_artist = get_ini_value(ini_path, section, "artistid")
        url_base = get_ini_value(ini_path, section, "urlenter")
        # 获取歌手的链接:https://music.163.com/artist?id=861777
        url_enter = url_base + id_artist
        # 访问链接
        headers = {
            'user-agent': "",
            'cookie': ''
        }
        html = requests.get(url_enter, headers=headers).text
        songs_id_name = re.findall("""<li><a href="(.*?)">(.*?)</a></li>""", html)
        print(0, "全部下载")
        songs_list = {}
        for num, song_id_name in enumerate(songs_id_name[:-6]):
            song_id = song_id_name[0].split("=")[1]
            song_name = song_id_name[1]
            # print(song_id, song_name)
            songs_list[num+1] = (song_id, song_name)
        for song_num, song_set in songs_list.items():
            print(song_num, song_set[1])
        b = input("请选择要下载的歌曲(非全部下载，歌曲序号用逗号隔开): ")
        if b.strip() == "0":  # 如果全部下载
            for song_set_download in songs_list.values():
                song_id_download = song_set_download[0]
                song_name_download = song_set_download[1]
                wangyiyun_download(ini_path, section, song_id_download, song_name_download)
        else:
            num_list = b.split(",")
            for num in num_list:
                song_set_download = songs_list[int(num.strip())]
                song_id_download = song_set_download[0]
                song_name_download = song_set_download[1]
                print(song_id_download)
                wangyiyun_download(ini_path, section, song_id_download, song_name_download)
