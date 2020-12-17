# 作者： pingyu
# 日期： 2020/9/15
# 时间： 14:56
import pandas as pd
from pandas.core.frame import DataFrame
from MultiObjectiveDispatch.entity import LoadTask

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


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
    # TODO 单辆车开单/时间窗口内多辆车同时开单
    for i in range(0, n):

        # print("这是第 %d " % i)
        # 一辆车所有的装车清单候选集
        candidate_set = []
        # 一份打包好的货物list
        candidate_for_one_truck = []
        # 初始化字典
        load_task_candidate[truck.loc[i]['car_mark']] = []
        # 取出和当前车次的城市和品名相同的货物
        stock_list_city_commodity = stock_data[(stock_data['城市'] == truck.loc[i]['city']) & (stock_data['品名'] == truck.loc[i]['big_commodity_name'])]
        # 取出可发重量
        can_be_sent_weight = stock_list_city_commodity['actual_weight'].tolist()
        # 取出单件重量
        print(truck.loc[i]['city'], truck.loc[i]['big_commodity_name'])

        if truck.loc[i]['big_commodity_name'] != '线材' and truck.loc[i]['big_commodity_name'] != '型钢' and truck.loc[i]['big_commodity_name'] != '螺纹':
            stock_list_city_commodity = stock_list_city_commodity[stock_list_city_commodity['unit_weight'] > 4.9]

        weight_unit = stock_list_city_commodity['unit_weight'].tolist()

        print(weight_unit)

        # 拿到最小的单件重量
        min_weight = min(weight_unit)

        # 把车次的载重上下限加入当前已分类货物信息中
        weight_up = truck.loc[i]['load_weight']
        # 把车次载重下限设置为上限的 80%
        weight_down = weight_up * 0.8
        # 得到最大单个候选集长度
        longest_iteration = weight_up//min_weight

        # print(weight_up, weight_down, load_task_candidate.keys())

        # TODO 库存更新：如果前一辆车已经确定装车货物，需在库存中减去已发货物

        # 根据重量规则生成候选集
        candidate_for_one_truck = dfs_pre_candidate(stock_list_city_commodity, weight_up, weight_down)

        # 将当前车次的候选集作为 value 存入字典
        load_task_candidate[truck.loc[i]['car_mark']] = candidate_for_one_truck
        # if len(candidate_for_one_truck) == 0:
        #     raise Exception('该车次无可分配货物')

        print(load_task_candidate)
    return load_task_candidate


def dfs_pre_candidate(weight_list, weight_up, weight_down):
    """
    深度搜索实现枚举过程
    :param weight_list: 当前经过筛选的库存数据
    :param weight_up: 当前车次载重上限
    :param weight_down: 当前车次载重下限
    :return candidate_set: 当前车次所有可装载的预装车清单
    """
    if weight_list.empty:
        return None

    pre_load_task_candidate = []

    print(weight_up, weight_down)

    def dfs_enumerate_search(l1, left, right):
        """
        枚举搜索
        :param l1: 当前满足重量要求的临时 dataframe
        :param left: 左指针
        :param right: 右指针
        :return:
        """

        # print(len(candidate_set))
        # 当前这个candidate里所有货物的总重量
        pre_candidate_weight_sum = l1.weight.sum()

        if weight_down <= pre_candidate_weight_sum <= weight_up:
            l1_list = list(l1.good_in_stock_index_list)
            pre_load_task_candidate.append(l1_list)
            # print(pre_load_task_candidate)
        elif pre_candidate_weight_sum > weight_up or left > right:
            return
        for j in range(0, right-left+1):
            l1_index = weight_l1.loc[left+j]['good_in_stock_index_list']
            l1_temp = weight_l1[weight_l1['good_in_stock_index_list'] == l1_index]
            dfs_enumerate_search(l1.append(l1_temp, ignore_index=True), left+j+1, len(good_in_stock_index)-1)

    # 取出已分类货物的index方便定位，此index即为当前类别下货物index
    good_in_stock_index = weight_list.index
    # 把所有货物在stock表中的index和weight取出，转换为list数组，这里的index是唯一定义货物的index
    good_in_stock_index_list = list(good_in_stock_index)
    weight = list(weight_list['unit_weight'])
    # 组合这两个list构建一个字典，其中index_list是所有可发货物下标，weight是货物对应的重量
    weight_temp = {'good_in_stock_index_list': good_in_stock_index_list, 'weight': weight}
    # weight_l1只包含原dataframe的货物下标和对应的货物重量
    weight_l1 = DataFrame(weight_temp)

    for i in range(len(good_in_stock_index)):
        dfs_enumerate_search(weight_l1[weight_l1['good_in_stock_index_list'] == good_in_stock_index[i]], 1, len(good_in_stock_index)-1)

    for ind in range(len(pre_load_task_candidate)):
        print(pre_load_task_candidate[ind], list(weight_l1[weight_l1['good_in_stock_index_list'] == pre_load_task_candidate[ind][0]]['weight']))
    print(pre_load_task_candidate)

    return pre_load_task_candidate
