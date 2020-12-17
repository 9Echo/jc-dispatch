# 作者： pingyu
# 日期： 2020/10/15
# 时间： 14:10

import pandas as pd


def sum_weighted(priority, weight, order):
    """
    三个目标函数对应的线性加权函数
    :param priority: 优先级
    :param weight: 占重比
    :param order: 拆单数量
    :return: score值
    """

    sum_func = 0
    # 设置三个优化目标的权重值
    weight_pri = 10
    weight_wei = 8
    weight_order = 2

    sum_func = weight_pri * priority + weight_wei * weight + weight_order * order

    return sum_func


def weighted_sum_method(stock, load_task_candidate, truck):
    """
    多目标求解法一：线性加权法
    :param stock: 已处理过的内存数据；数据格式：DataFrame
    :param load_task_candidate: 即为所有车辆生成的总装车清单候选集；数据格式：{‘car_mark':candidate_set[[],[]]}
    :param truck: 数据格式：DataFrame
    :return: load_task: DataFrame, 生成的装车清单；数据格式：{'car_mark':candidate_for_one []}
    """

    col = stock.columns
    load_task = pd.DataFrame(columns=col)
    # 初始化车牌号字段
    load_task['car_mark'] = ''

    n_truck = len(truck)
    # 取出某一车次的所有装车清单候选集
    # TODO 只采用前两辆车数据
    actual_weight = 0
    for i in range(0, n_truck):
        car_mark = truck.loc[i]['car_mark']
        # 当前车辆对应的预装车清单候选集
        pre_load_task_candidate_truck = load_task_candidate[car_mark]

        if len(pre_load_task_candidate_truck) == 0:
            print('当前无可分配货物')
            return load_task

        # 获取当前车次载重
        weight_up = truck.loc[i]['load_weight']

        # 该车辆所有的可装车清单候选集长度（即分货的可能方式）
        n_load_task = len(pre_load_task_candidate_truck)
        # 该车次对应的最大线性分值
        max_score = 0
        # 记录当前车次对应的每个预装车清单候选集的分值
        sum_list_weight = []
        # 遍历该装车清单候选集
        for j in range(n_load_task):
            # load_one_candidate:[] 表示其中一种的装车清单
            load_one_candidate = pre_load_task_candidate_truck[j]
            # 该候选集对应的货物个数
            n_one_candidate = len(load_one_candidate)
            # 遍历该装车清单里的货物信息,包括优先级、重量
            sum_priority = 0
            sum_weight = 0
            sum_order = 0

            for k in range(n_one_candidate):
                # 1. 计算优先级数值
                index = load_one_candidate[k]
                sum_priority += stock.loc[index]['priority']
                # 2. 计算单个候选集总重量
                sum_weight += stock.loc[index]['unit_weight']

            # 计算单个候选集的score值
            score = sum_weighted(sum_priority, sum_weight/weight_up, sum_order)
            sum_list_weight.append(score)

        max_score = max(sum_list_weight)
        # 分值最高的候选集对应的数组
        ind = sum_list_weight.index(max_score)

        """
        1. 当前数组里是原库存信息表DataFrame的index，根据该index取出库存数据，生成新的load_task
        2. 当前车次的预装车清单候选集里的index和每个预装车清单候选集分数的index是一样的
        3. pre_load_task：根据max_score从预装车清单候选集里取出该车次的预装车清单
        [[],[],...,[]]  →  []
        """

        pre_load_task = pre_load_task_candidate_truck[ind]
        # 生成load_task
        n_load_task_ind = len(pre_load_task)

        for stock_ind in range(n_load_task_ind):
            pre_load_task_truck = stock.iloc[pre_load_task[stock_ind]: pre_load_task[stock_ind] + 1]
            pre_load_task_truck['car_mark'] = ''
            pre_load_task_truck = pre_load_task_truck.reset_index(drop=True)
            pre_load_task_truck.loc[0, ['car_mark']] = car_mark

            actual_weight += pre_load_task_truck.loc[0, ['unit_weight']]

            load_task = load_task.append(pre_load_task_truck, ignore_index=True)

            print(actual_weight)

    return load_task
