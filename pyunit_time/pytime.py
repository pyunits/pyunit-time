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

    def __init__(self, current_time=None):
        super().__init__()
        self.current_time = arrow.get(current_time)
        self.key = None
        self.notify()

    def subscribe(self, observer: IObserver):
        self.observers.append(observer)

    def unsubscribe(self, observer: IObserver):
        self.observers.remove(observer)

    def notify(self, *args, **kwargs):
        self.observers.append(Years())

    def parse(self, string, **kwargs) -> list:
        dicts = []
        keys = filters_string(string, **kwargs)
        for key in keys:
            deal_date = self._deal_time(key)
            dicts.append({'key': key, 'date': deal_date})
        return dicts

    def _deal_time(self, key) -> datetime:
        update_time = self.current_time
        self.key = key
        for o in self.observers:
            update_time = o.notify(self, time=update_time)
        return update_time.datetime
