#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/21 17:19
# @Author: Jtyoui@qq.com
# @Notes : 处理中文时间
from pyunit_gof import IObservable, IObserver
from .filters import filters_string
from .retime import *
import arrow
import datetime


class Time(IObservable):

    def __init__(self, current_time=None, formats="YYYY-MM-DD HH:mm:ss"):
        super().__init__()
        self.format = formats
        self.current_time = arrow.get(current_time)  # 设置当前时间
        self.key = None
        self.notify()

    def subscribe(self, observer: IObserver):
        self.observers.append(observer)

    def unsubscribe(self, observer: IObserver):
        self.observers.remove(observer)

    def notify(self, *args, **kwargs):
        self.observers.append(Years())  # 处理年份
        self.observers.append(SolarHoliday())  # 处理公历的节日
        self.observers.append(LunarHoliday())  # 处理农历的节日
        self.observers.append(SpecialHoliday())  # 处理特殊要计算的节日
        self.observers.append(SolarTerm24())  # 处理24节气
        self.observers.append(Months())  # 处理月份
        self.observers.append(Weeks())  # 处理星期
        self.observers.append(Days())  # 处理日期
        self.observers.append(Hours())  # 处理小时
        self.observers.append(Minutes())  # 处理分钟
        self.observers.append(Seconds())  # 处理秒钟

    def parse(self, string, **kwargs) -> list:
        """处理字符串，提取时间类型"""
        dicts = []
        keys = filters_string(string, **kwargs)
        for key in keys:
            deal_date = self._deal_time(key)
            dicts.append({'key': key, 'keyDate': deal_date, 'baseDate': self.current_time.format(self.format)})
        return dicts

    def _deal_time(self, key) -> datetime:
        update_time = self.current_time
        self.key = key
        for o in self.observers:
            update_time = o.notify(self, time=update_time)
        return update_time.format(self.format)
