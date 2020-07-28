#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
"""=================================================
@Project -> File    : 20200714 -> main_1.py
@IDE     : PyCharm
@Author  : Aimee
@Date    : 2020/7/24 10:25
@Desc    :
================================================="""
import test
import gloval


if __name__ == '__main__':
    test.change_x()
    gloval.x = 3 + gloval.x
    print(gloval.x)
