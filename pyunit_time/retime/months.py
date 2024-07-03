# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:42
# @Author: Jtyoui@qq.com
# @Notes : 处理月份
from ..observer import IObserver
import re

# 中国的月份对应数字
chinese_mon_number = {
    '零': '0',
    '正': '1',
    '一': '1',
    '二': '2',
    '两': '2',
    '三': '3',
    '四': '4',
    '五': '5',
    '六': '6',
    '七': '7',
    '八': '8',
    '九': '9',
    '十': '10',
    '冬': '11',
    '腊': '12',
}


class Months(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.set_number_month()
        self.set_shift_month()
        return self.time

    def set_number_month(self):
        rule = '(10|11|12|0?[1-9])(?=月)'
        match = re.search(rule, self.key)
        if match:
            mon = int(match.group())
            if '今天' in self.key:
                self.time = self.time.replace(month=mon)  # 如果有月份并且有今天
            else:
                self.time = self.time.replace(month=mon, day=1)

    def set_shift_month(self):
        """处理上个月之类的
        比如处理： 上个月、上上个月、上3个月、2个月以前等等
        """
        rule = r'([上下]+)个?月|[上下](\d+)个?月|(\d+)个?月[以之]?[前后内]'
        match = re.search(rule, self.key)
        if match:
            length = match.group(match.lastindex)
            if not length.isdigit():
                length = len(length)
            else:
                length = int(length)

            # 判断是否是之前的
            for tip in ["上", "前"]:
                value = match.group()
                if tip in value:
                    length = -length

            self.time = self.time.shift(months=length)
