# 作者： pingyu
# 日期： 2020/9/15
# 时间： 14:56
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def deal_stock(data):
    """

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
    # TODO

    return data


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
        # 取出可发件数和可发重量
        can_be_sent_quality = stock_list_city_commodity['可发件数'].tolist()
        can_be_sent_weight = stock_list_city_commodity['可发重量'].tolist()
        # 计算单件重量
        weight_unit = []
        for j in range(len(index)):
            if stock_list_city_commodity.loc[index[j]]['可发件数']:
                weight_unit.append(stock_list_city_commodity.loc[index[j]]['可发重量'] / stock_list_city_commodity.loc[index[j]]['可发件数'])
                # weight_unit.append(can_be_sent_weight[j] / can_be_sent_quality[j])
            else:
                weight_unit.append(stock_list_city_commodity.loc[index[j]]['可发重量'])
                # weight_unit.append(can_be_sent_weight[j])

        # 把货物单件重量和车次的载重上下限加入当前已分类货物信息中
        weight_unit_up = [truck.loc[i]['load_weight']] * len(index)
        stock_list_city_commodity['weight_unit_up'] = weight_unit_up

        stock_list_city_commodity['weight_unit'] = weight_unit

        weight_unit_down = []
        for ind in range(len(weight_unit)):
            weight_unit_down.append(weight_unit[ind] * 0.8)
        stock_list_city_commodity['weight_unit_down'] = weight_unit_down
        # print(stock_list_city_commodity)

        # 开始生成装车清单集合
        sum = 0

        for j in range(len(index)):
            for num in range(can_be_sent_quality[j]):
                if sum <= weight_unit_up[j]:
                    sum += can_be_sent_weight[j]
                    candidate_for_one_truck.append(index[j])
                else:
                    sum = 0
                    candidate_set.append(candidate_for_one_truck)
                    candidate_for_one_truck = []
        print(candidate_set)




    return load_task_candidate


def rank(load_task_candidate):

    load_task_rank = load_task_candidate


    return load_task_rank


def dispatch(load_task_rank, truck):

    load_task = {}

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
