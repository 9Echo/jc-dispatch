#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/2 9:59
# @Author  : \lambda
# @File    : Truck.py
# @Software: PyCharm

import pandas as pd


def get_truck():
    truck = pd.read_excel("../truck.xls")
    return truck
