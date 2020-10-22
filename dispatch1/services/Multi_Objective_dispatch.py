# 作者： pingyu
# 日期： 2020/9/15
# 时间： 14:56
import pandas as pd
from dispatch1.entity import LoadTask

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def deal_stock(data):
    """
    转化优先级、设置可发重量，将所有货物按单件拆开
    :param data: 原始库存数据
    :return: stock_data: 数据处理后的库存数据
    """
    if data.empty:
        raise Exception('输入列表为空')

    # 将优先发运转换为对应的优先级数字
    # print(data.head())
    data = data.fillna(0)
    data['priority'] = ''
    data['priority'].loc[data['优先发运'] == '超期清理'] = 2
    data['priority'].loc[data['优先发运'] == '客户催货'] = 1
    data['priority'].loc[data['优先发运'] == 0] = 0
    # print('-------------------------')
    # print(data.head())

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


def generate_candidate(stock_data, truck):
    """

    :param stock_data:
    :param truck:
    :return:
    load_task_candidate = {key:value}
    key: driver_id
    value:[[list]]
    """

    if truck.empty:
        raise Exception('输入列表为空')

    # 根据当前车次的品种和目的地，筛选货物，符合条件的货物生成装车清单候选集
    load_task_candidate = {}

    n = len(truck)
    # 遍历车次列表
    for i in range(n):

        # 一辆车所有的装车清单候选集
        candidate_set = []
        # 一份打包好的货物list
        candidate_for_one_truck = []
        # 初始化字典
        load_task_candidate[truck.loc[i]['driver_id']] = candidate_set
        # 取出和当前车次的城市和品名相同的货物
        stock_list_city_commodity = stock_data[(stock_data['城市'] == truck.loc[i]['city']) & (stock_data['品名'] == truck.loc[i]['big_commodity_name'])]
        # 取出已分类货物的index方便定位，此index即为当前类别下货物行数
        index = stock_list_city_commodity.index
        # 取出可发重量
        can_be_sent_weight = stock_list_city_commodity['actual_weight'].tolist()
        # 取出单件重量
        weight_unit = stock_list_city_commodity['unit_weight'].tolist()
        # 拿到最小的单件重量
        min_weight = min(weight_unit)

        # 把车次的载重上下限加入当前已分类货物信息中
        weight_up = truck.loc[i]['load_weight']
        # 把车次载重下限设置为上限的 80%
        weight_down = weight_up * 0.8

        # 得到最大单个候选集长度
        longest_iteration = weight_up//min_weight

        # 通过候选集长度进行遍历
        for long_iter in range(longest_iteration):
            # 当长度为1时，只需遍历一次货物列表即可
            if long_iter == 0:
                for j in range(len(index)):
                    candidate_for_one_truck = []
                    current_weight = stock_list_city_commodity.loc[index[j]]['unit_weight']
                    if weight_up >= current_weight >= weight_down:
                        candidate_for_one_truck.append(index[j])
                        candidate_for_one_truck.append(current_weight)
                        candidate_set.append(candidate_for_one_truck)
            else:
                # 遍历两次当前已分类货物列表
                for j in range(len(index)):
                    for j_temp in range(j+1, len(index)):
                        candidate_for_one_truck = []
                        sum_weight = 0
                        while len(candidate_for_one_truck) <= long_iter+1:
                            if sum_weight + stock_list_city_commodity.loc[index[j]]['unit_weight'] <= weight_up:
                                candidate_for_one_truck.append(index[j])
                                sum_weight += stock_list_city_commodity.loc[index[j]]['unit_weight']

                        if sum_weight >= weight_down:
                            candidate_for_one_truck.append(sum_weight)
                            candidate_set.append(candidate_for_one_truck)


        # 开始生成装车清单集合

        # 遍历当前已分类货物列表

            if sum_weight <= weight_up:
                candidate_for_one_truck.append(index[j])
                sum_weight += stock_list_city_commodity.loc[index[j]]['unit_weight']
            elif sum_weight > weight_up:
                sum_weight = 0
                candidate_for_one_truck = []

        # 将当前车次的候选集作为 value 存入字典
        load_task_candidate[truck.loc[i]['driver_id']] = candidate_set

        # print(load_task_candidate)
    return load_task_candidate


def rank(load_task_candidate):

    load_task_rank = load_task_candidate


    return load_task_rank


def dispatch(load_task_rank, truck):

    load_task = LoadTask()

    return load_task


if __name__ == "__main__":

    # 输入当天库存数据
    stock_day = pd.read_excel("./test_stock.xls")

    # 库存数据预处理
    stock_data = deal_stock(stock_day)

    # 车辆数据（非真实数据）
    truck = pd.read_excel("./truck.xls")

    # 根据库存为当前车次（30辆车）的每一辆车生成装车清单候选集
    load_task_candidate = generate_candidate(stock_data, truck)

    # 利用rank函数为装车清单候选集排序
    load_task_rank = rank(load_task_candidate)

    # 优先将rank值高的候选集与车次进行匹配
    load_task_dispatch = dispatch(load_task_rank, truck)
