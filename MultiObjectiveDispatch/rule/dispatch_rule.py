# 作者： pingyu
# 日期： 2020/10/1
# 时间： 15:38   


def consumer_filter(stock_list):
    """
    优先级分货规则：
    1.根据催货1级和催货2级和超期将货物分为3档
    2.按照先催货后超期的顺序将排序结果合并
    """
    # 将库存分为催货库存和其他库存
    if not stock_list:
        return stock_list

    hurry_consumer_list = stock_list
    # 排序后的催货列表
    new_hurry_stock_list = []
    # 对最高优先级进行排序
    hurry_stock_list = [stock for stock in stock_list if stock.priority == 1]
    left_stock_list = stock_list[len(hurry_stock_list):]
    new_hurry_stock_list += sort_stock_list(hurry_stock_list, hurry_consumer_list)
    # 对第二优先级进行排序
    hurry_stock_list = [stock for stock in left_stock_list if stock.priority == 2]
    left_stock_list = left_stock_list[len(hurry_stock_list):]
    new_hurry_stock_list += sort_stock_list(hurry_stock_list, hurry_consumer_list)
    # 如果没有一级二级货物，结束轮询操作
    if not new_hurry_stock_list:
        return stock_list
    # 队列第一次被抽到的客户移到队列末尾
    first_consumer = new_hurry_stock_list[0].consumer
    first_index = 0
    while first_index < len(hurry_consumer_list):
        if hurry_consumer_list[first_index] == first_consumer:
            break
        else:
            first_index += 1
    hurry_consumer_list.append(hurry_consumer_list[first_index])
    hurry_consumer_list.pop(first_index)

    return new_hurry_stock_list + left_stock_list


def sort_stock_list(stock_list, hurry_consumer_list):
    """
    根据催货客户列表给当前库存排序
    """
    # 列表为空时直接返回
    if not stock_list:
        return []
    # 构建催货库存字典, 每个客户对应一个库存列表
    stock_dict = {}
    for stock in stock_list:
        stock_dict.setdefault(stock.consumer, []).append(stock)
    # 库存排序
    new_stock_list = []
    for consumer in hurry_consumer_list:
        if consumer in stock_dict:
            new_stock_list.extend(stock_dict[consumer])
    return new_stock_list

