# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:42
# @Author: Jtyoui@qq.com
# @Notes : 处理小时
from ..observer import IObserver
import re

DayHour = {
    '黎明': 3,
    '早上': 8,
    '上午': 10,
    '中午': 12,
    '午间': 12,
    '下午': 15,
    '午后': 15,
    '晚上': 18,
    '傍晚': 18,
    '晚间': 20,
    '深夜': 23,
}


class Hours(IObserver):
    def __init__(self):
        self.key = None
        self.time = None
        self.current_time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.current_time = observable.current_time
        self.time = kwargs['time']
        self.set_number_hour()
        self.set_replace_hour()
        self.set_shift_hour()
        self.set_day_hour()
        return self.time

    def set_replace_hour(self):
        """识别普通的几点"""
        rule = '(?<![周星期])([0-2]?[0-9])(?=(点|时))'
        match = re.search(rule, self.key)
        if match:
            hour = int(match.group())
            self.time = self.time.replace(hour=hour)

    def set_shift_hour(self):
        """识别关键词特定的时间"""
        match = re.search('|'.join(DayHour.keys()), self.key)
        if match and self.time.hour == self.current_time.hour:  # 保证时间没有被改变过
            hour = DayHour[match.group()]
            self.time = self.time.shift(hours=hour)
        else:
            h = self.time.hour
            if re.search('中午|午间', self.key):  # 判断中午是12-15点
                if 0 <= h <= 3:
                    self.time = self.time.shift(hours=12)  # 判断下午是15-18点
            elif re.search('下午|午后', self.key):
                if 3 <= h <= 6:
                    self.time = self.time.shift(hours=12)
            elif re.search('晚上|夜间|夜里|今晚', self.key):  # 判断晚上是18点到24点
                if 6 <= h <= 12:
                    self.time = self.time.shift(hours=12)
            elif re.search('半夜|深夜|凌晨', self.key):  # 判断半夜凌晨0点到第二天早上8点
                if 0 <= h <= 8:
                    self.time = self.time.shift(days=1)

    def set_day_hour(self):
        """设置时间能改变天数"""
        match = re.search('(明晚)|(昨晚)|(前晚)', self.key)
        if match:  # 判断明天晚上
            if match.lastindex == 1:
                day = 1
            elif match.lastindex == 2:
                day = -1
            elif match.lastindex == 3:
                day = -2
            else:
                day = 0
            self.time = self.time.shift(days=day)
            if 6 <= self.time.hour <= 12:
                self.time = self.time.shift(hours=12)
            elif self.time.hour == self.current_time.hour:
                self.time = self.time.replace(hour=18)

    def set_number_hour(self):
        """设置多少个小时以前还是以后"""
        rule = r'\d+(?=个?小时[以之]?[前后内])'
        match = re.search(rule, self.key)
        if match:
            h = int(match.group())
            h = -h if ('前' in self.key) else h
            self.time = self.time.shift(hours=h)

        rule = r'(在|再)过(\d+)小时'
        match = re.search(rule, self.key)
        if match:
            h = int(match.group(2))
            self.time = self.time.shift(hours=h)
