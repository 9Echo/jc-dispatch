#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/31 16:38
# @Author  : \lambda
# @File    : deal_stock.py
# @Software: PyCharm

import pandas as pd


def deal_stock(data):
    """
    转化优先级、设置可发重量，将所有货物按单件拆开
    :param data: 原始库存数据
    :return: stock_data: 数据处理后的库存数据
    """
    if data.empty:
        raise Exception('输入列表为空')

    # 将优先发运转换为对应的优先级数字
    data = data.fillna(0)
    data['priority'] = ''
    data['priority'].loc[data['优先发运'] == '超期清理'] = 1
    data['priority'].loc[data['优先发运'] == '客户催货'] = 2
    data['priority'].loc[data['优先发运'] == 0] = 0

    # 将货物拆分成最小不可再拆形式（即每一条货物信息中的重量都小于等于最小载重）
    data['actual_number'] = data['可发件数'] + data['需开单件数']
    data['actual_weight'] = data['可发重量'] + data['需开单重量']
    data['unit_weight'] = round(data['actual_weight'] / data['actual_number'])
    data = data.loc[data['actual_number'] > 0]

    all_stock_list = pd.DataFrame()

    for i in range(len(data)):
        a = data.iloc[i]
        b = pd.DataFrame(a).T
        # 第37列是可发数量
        number = data.iloc[i, 37]
        all_stock_list = all_stock_list.append([b] * number)

    all_stock_list.reset_index(drop=True, inplace=True)
    # all_stock_list['actual_number'] = 1

    return all_stock_list
