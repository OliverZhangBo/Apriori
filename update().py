#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 16:24
# @Author  : Arrow and Bullet
# @FileName: update().py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/qq_41800366

dict = {'Name': 'Zara', 'Age': 7}
dict2 = {'Sex': 'female'}
dict.update(dict2)
print(dict)  # 结果 {'Name': 'Zara', 'Age': 7, 'Sex': 'female'}

dict = {'Name': 'Zara', 'Age': 7}
dict2 = {'Age': 18, 'Sex': 'female'}
dict.update(dict2)
print(dict)  # 结果 {'Name': 'Zara', 'Age': 18, 'Sex': 'female'}