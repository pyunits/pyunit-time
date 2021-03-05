# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:42
# @Author: Jtyoui@qq.com
# @Notes : 处理日期
from ..observer import IObserver
import re


class Days(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.set_replace_day()
        self.set_number_day()
        self.set_shift_day()
        self.deal_word_day()
        return self.time

    def set_replace_day(self):
        """处理替换的天数"""
        rule = r'(?<=最后)(\d+)(?=天)|(?<=第)(\d+)(?=天)'
        match = re.search(rule, self.key)
        if match:
            day = int(match.group())
            if match.lastindex == 2:  # 第x天
                replace_day = day
            else:  # 最后x天
                replace_day = self.time.ceil('month').date().day - day + 1
            self.time = self.time.replace(day=replace_day)

    def set_number_day(self):
        """识别12日之类的数字日期"""
        rule = r'(?<!\d)([0-3][0-9]|[1-9])(?=[日号])'
        match = re.search(rule, self.key)
        if match:
            day = int(match.group())
            self.time = self.time.replace(day=day)

    def set_shift_day(self):
        """识别要移动的天数

        比如处理：多少天以前、多少天以后
        """
        rule = r'\d+(?=(天|日|号)[以之]?[前后内])|(?<=[^最]后)\d+(?=天)|(?<=前)\d+(?=天)'
        match = re.search(rule, '@' + self.key)  # 加上@是保证后x天不是第一个出现的字符，满足[^最]后语法
        if match:
            day = int(match.group())
            day = -day if ('前' in self.key) else day
            self.time = self.time.shift(days=day)

    def deal_word_day(self):
        """处理带有文字的日期

        比如：前天、昨天等
        """
        word = {
            '大前天': -3,
            '前天': -2,
            '昨天': -1,
            '今天': 0,
            '明天': 1,
            '后天': 2,
            '外天': 3,
            '大后天': 3,
        }
        match = re.finditer('|'.join(word.keys()), self.key)
        for m in match:
            self.time = self.time.shift(days=word[m.group()])
