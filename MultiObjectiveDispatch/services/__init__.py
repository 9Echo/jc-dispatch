# 作者： pingyu
# 日期： 2020/10/1
# 时间： 19:10   
import pandas as pd

from MultiObjectiveDispatch.DAO.Stock import get_stock_day
from MultiObjectiveDispatch.DAO.Truck import get_truck
from MultiObjectiveDispatch.services.deal_stock import deal_stock
from MultiObjectiveDispatch.services.Generate_pre_load_task_candidate import generate_candidate
from MultiObjectiveDispatch.services.Weighted_Sum_Method import weighted_sum_method

if __name__ == "__main__":

    # 读取当天库存数据
    stock_day = get_stock_day()

    # 库存数据预处理
    stock_data = deal_stock(stock_day)

    # 车辆数据（非真实数据）
    truck = get_truck()

    # 根据库存为当前车次生成装车清单候选集
    load_task_candidates = generate_candidate(stock_data, truck)

    # 多目标优化求解法1：线性加权法
    weighted_sum_load_task = weighted_sum_method(stock_data, load_task_candidates, truck)
    print(weighted_sum_load_task)
