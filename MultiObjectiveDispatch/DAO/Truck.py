#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/2 9:59
# @Author  : \lambda
# @File    : Truck.py
# @Software: PyCharm

import pandas as pd


def get_truck():
    truck0 = pd.read_excel("../truck0_8.xls")
    truck1 = pd.read_excel("../truck1.xlsx")
    return truck1
