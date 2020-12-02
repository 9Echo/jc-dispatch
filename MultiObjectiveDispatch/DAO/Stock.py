#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 16:26
# @Author  : \lambda
# @File    : Stock.py
# @Software: PyCharm

import pandas as pd


def get_stock_day():
    stock_day = pd.read_excel("../test_stock.xls")
    return stock_day
