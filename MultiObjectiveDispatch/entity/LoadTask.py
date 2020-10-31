# 作者： pingyu
# 日期： 2020/10/1
# 时间： 14:05


class LoadTask:
    """车次类"""

    def __init__(self):
        self.load_task_id = None  # 所属车次号
        # 优先级
        self.priority = 0
        # 发货通知单重量
        self.weight = 0
        # 发货通知单件数
        self.count = 0
        # 城市
        self.city = None
        # 区县
        self.end_point = None
        # 大品种
        self.big_commodity = None
        # 品种
        self.commodity = None
        # 发货通知单号
        self.notice_num = None
        # 订单项次号
        self.oritem_num = None
        # 收货用户
        self.consumer = None
        # 规格
        self.standard = None
        # 材质
        self.sgsign = None
        # 出库仓库
        self.outstock_code = None
        # 入库仓库
        self.instock_code = None
        # 收货地址
        self.receive_address = None
        # 父Id
        self.parent_load_task_id = None
        # 最新挂单时间
        self.latest_order_time = None
        # 库存号
        self.notice_stock_info_id = None

