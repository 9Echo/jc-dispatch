# 作者： pingyu
# 日期： 2020/9/15
# 时间： 14:56
import pandas as pd
from pandas.core.frame import DataFrame
from MultiObjectiveDispatch.entity import LoadTask

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
    key: car_mark
    value:[[list]]
    """

    if truck.empty:
        raise Exception('输入列表为空')

    # 根据当前车次的品种和目的地，筛选货物，符合条件的货物生成装车清单候选集
    load_task_candidate = {}

    n = len(truck)
    # 遍历车次列表
    for i in range(0, 1):

        # 一辆车所有的装车清单候选集
        candidate_set = []
        # 一份打包好的货物list
        candidate_for_one_truck = []
        # 初始化字典
        load_task_candidate[truck.loc[i]['car_mark']] = candidate_set
        # 取出和当前车次的城市和品名相同的货物
        stock_list_city_commodity = stock_data[(stock_data['城市'] == truck.loc[i]['city']) & (stock_data['品名'] == truck.loc[i]['big_commodity_name'])]
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

        # print(stock_list_city_commodity)
        # 通过候选集长度进行遍历

        # 根据重量规则生成候选集
        candidate_for_one_truck = dfs_candidate(stock_list_city_commodity, weight_up, weight_down)

        # 将当前车次的候选集作为 value 存入字典
        load_task_candidate[truck.loc[i]['car_mark']] = candidate_set

        # print(load_task_candidate)
    return load_task_candidate


def dfs_candidate(weight_list, weight_up, weight_down):
    """
    深度搜索实现枚举过程
    :param weight_list: 当前经过筛选的库存数据
    :param weight_up: 当前车次载重上限
    :param weight_down: 当前车次载重下限
    :return candidate_set: 当前车次所有可装载的预装车清单
    """
    if weight_list.empty:
        return None

    candidate_set = []

    def dfs(l1, l, r):
        """
        枚举
        :param l1: 当前满足重量要求的临时dataframe
        :param l: 左指针
        :param r: 右指针
        :return:
        """
        n = l1.weight.sum()
        # print(weight_up, weight_down, n)
        if weight_down <= n <= weight_up:
            l1_list = list(l1.index_weight)
            candidate_set.append(l1_list)
            # print(candidate_set)
        elif n > weight_up or l > r:
            return
        for j in range(0, r-l+1):
            l1_index = weight_l1.loc[l+j]['index_weight']
            l1_temp = weight_l1[weight_l1['index_weight'] == l1_index]
            dfs(l1.append(l1_temp, ignore_index=True), l+j+1, r-1)

    # 取出已分类货物的index方便定位，此index即为当前类别下货物index
    index = weight_list.index
    index_weight = list(index)
    weight = list(weight_list['unit_weight'])
    weight_temp = {'index_weight': index_weight, 'weight': weight}
    # weight_l1只包含原dataframe的货物下标和对应的货物重量
    weight_l1 = DataFrame(weight_temp)

    for i in range(len(index)):
        dfs(weight_l1[weight_l1['index_weight'] == index[i]], 1, len(index)-1)

    for ind in range(len(candidate_set)):
        print(candidate_set[ind], list(weight_l1[weight_l1['index_weight'] == candidate_set[ind][0]]['weight']))
    # print(candidate_set)
    return candidate_set


def dispatch(load_task_candidate, truck):

    # load_task = LoadTask()
    load_task = []

    return load_task


if __name__ == "__main__":

    # 输入当天库存数据
    stock_day = pd.read_excel(r"D:\Users\pc\PycharmProjects\jc-dispatch\MultiObjectiveDispatch\test_stock.xls")

    # 库存数据预处理
    stock_data = deal_stock(stock_day)

    # 车辆数据（非真实数据）
    truck = pd.read_excel("D://Users//pc//PycharmProjects//jc-dispatch//MultiObjectiveDispatch//truck.xls")

    # 根据库存为当前车次（30辆车）的每一辆车生成装车清单候选集
    load_task_candidates = generate_candidate(stock_data, truck)

    # 优先将rank值高的候选集与车次进行匹配
    load_task_dispatch = dispatch(load_task_candidates, truck)
