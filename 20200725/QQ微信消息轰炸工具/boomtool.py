#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
"""=================================================
@Project -> File    : 20200714 -> boomtool.py
@IDE     : PyCharm
@Author  : Aimee
@Date    : 2020/7/25 14:41
@Desc    :只能发送中文，发送英文的话可能显示不全
================================================="""
import time
from pynput.keyboard import Key, Controller as key_cl  # 键盘控制器
from pynput.mouse import Button, Controller as mouse_cl  # 鼠标控制器


# 键盘控制函数
def keyboard_input(string_input):
    keyboard = key_cl()  # 接管键盘消息
    keyboard.type(string_input)  # 设置数据发送类型
    time.sleep(0.2)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


# 鼠标控制函数
def mouse_click():
    mouse = mouse_cl()  # 接管鼠标消息
    mouse.press(Button.left)  # 按压鼠标左键
    mouse.release(Button.left)  # 松开鼠标左键


# 文字信息的发送
def send_msg(num, string_msg):
    print("3S后正式开始执行程序...")
    time.sleep(3)  # 休眠3秒

    for i in range(num):
        keyboard_input(string_msg)  # 设置输入的文字内容
        # mouse_click()               # 鼠标左键点击


def main():
    send_msg(5, "人生，只要能照亮某个角落就够了。")


if __name__ == '__main__':
    print(200/12)
    # main()
