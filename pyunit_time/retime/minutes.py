# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:43
# @Author: Jtyoui@qq.com
# @Notes : 处理分钟
from pyunit_gof import IObserver
import re


class Minutes(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.set_number_minute()
        self.set_replace_minute()
        return self.time

    def set_number_minute(self):
        """设置多少个分钟以前还是以后"""
        rule = r'\d+(?=分钟?[以之]?[前后内])'
        match = re.search(rule, self.key)
        if match:
            m = int(match.group())
            m = -m if ('前' in self.key) else m
            self.time = self.time.shift(minutes=m)

    def set_replace_minute(self):
        """识别可替换的时间 """
        minute = None
        rule = '(?<=[点时])[0-5]?[0-9](?=分)'
        match = re.search(rule, self.key)
        if match and match.group().isdigit():  # 判断多少分钟
            minute = int(match.group())
        match = re.search('(?<=[点时])[123]刻', self.key)  # 判断多少刻钟
        if match:
            m = match.group()
            if m and m[0].isdigit():
                minute = 15 * int(m[0])
        elif re.search('(?<=[点时])半', self.key):  # 判断多少点半
            minute = 30
        if minute is not None:
            self.time = self.time.replace(minute=minute)
