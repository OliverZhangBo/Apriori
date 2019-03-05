#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 18:29
# @Author  : Arrow and Bullet
# @FileName: votesmart.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/qq_41800366
import votesmart


votesmart.apikey = "49024thereoncewassamanfromnantyck94040"

bills = votesmart.votes.getBillsByStateRecent()
for bill in bills:
    print(bill.title, bill.billId)