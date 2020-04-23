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
        self.set_number_second()
        self.set_replace_second()
        return self.time

    def set_number_second(self):
        """设置多少个秒以前还是以后"""
        rule = r'\d+(?=秒钟?[以之]?[前后内])'
        match = re.search(rule, self.key)
        if match:
            s = int(match.group())
            s = -s if ('前' in self.key) else s
            self.time = self.time.shift(seconds=s)

    def set_replace_second(self):
        """省略秒说法的时间：如19点10分30"""
        rule = '([0-9]+(?=秒))|((?<=分)[0-5]?[0-9])'
        match = re.search(rule, self.key)
        if match:
            second = int(match.group())
            self.time = self.time.replace(second=second)
