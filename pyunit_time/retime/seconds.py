# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:43
# @Author: Jtyoui@qq.com
# @Notes : 处理秒钟
from pyunit_gof import IObserver
import re


class Seconds(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        return self.time
