# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:42
# @Author: Jtyoui@qq.com
# @Notes : 处理小时
from pyunit_gof import IObserver
import re

day_break = 3  # 黎明
early_morning = 8  # 早
morning = 10  # 上午
noon = 12  # 中午、午间
afternoon = 15  # 下午、午后
night = 18  # 晚上、傍晚
lateNight = 20  # 晚、晚间
midNight = 23  # 深夜


class Hours(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        return self.time
