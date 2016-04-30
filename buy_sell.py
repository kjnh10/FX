# -*- coding: utf-8 -*-
import datetime
import api
from enum import Enum

class OrderType(Enum):
    Buy = 1
    Wait = 0
    Sell = -1

class Rate(object):
    start_at = datetime.datetime(2015, 10, 1, 10, 0, 0)
    bid = float(120.00)
    h24 = float(119.40)
    base_tick = float(0.01)

    @classmethod
    def get(cls, currency=None, start_at=None):
        return Rate()

    def get_rate(self, tick, is_add):
        if is_add:
            return self.bid + float(tick * self.base_tick)
        else:
            return self.bid - float(tick * self.base_tick)


class AIOrder(object):
    def __init__(self, order_type, limit, stop_limit):
        self.order_type = order_type
        self.limit = limit
        self.stop_limit = stop_limit


class AI(object):
    # 発注を決定する要素、24h平均との差がこの値以上で発注する。
    DIFF = 30
    # 発注時の利益確定レートを決定する要素
    LIMIT = 30
    # 発注時の損切りレートを決定する要素
    STOP_LIMIT = 30

    def __init__(self, rate):
        self.rate = rate

    def order(self):
        """
        発注する。
        """
        if self._can_order():
            order(self._get_order())

    def _can_order(self):
        """
        発注可能か返却
        rtype: bool
        """
        point = (self.rate.bid - self.rate.h24) / self.rate.base_tick
        return int(point / self.DIFF) not in [0]

    def _get_order(self):
        """
        発注クラスを返却
        rtype: AIOrder
        """
        limit_rate = self.rate.get_rate(AI.LIMIT, True)
        stop_limit_rate = self.rate.get_rate(AI.STOP_LIMIT, False)
        return AIOrder(self._get_order_type(), limit_rate, stop_limit_rate)

    def _get_order_type(self):
        if self.rate.bid > self.rate.h24:
            return OrderType.Buy
        if self.rate.h24 > self.rate.bid:
            return OrderType.Sell
        return OrderType.Wait


def order(ai_order):
    _base = "OrderDone:{}, Limit:{}, Stop-Limit:{}"
    print _base.format(ai_order.order_type,
                       ai_order.limit,
                       ai_order.stop_limit)

# レート取得
rate = Rate.get(currency='USDJPY', start_at=datetime.datetime.now())

# AI生成
ai = AI(rate)

# 発注
ai.order()

# >>> OrderDone:True, Limit:120.3, Stop-Limit:119.7
