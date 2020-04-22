# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:42
# @Author: Jtyoui@qq.com
# @Notes : 处理年份
from pyunit_gof import IObserver
import re


class Years(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.deal_number_year()
        self.deal_word_year()
        return self.time

    def deal_number_year(self):
        """处理带有数字的年,只能匹配2位数字或者四位数字

        比如： 两位数字的年份只能是19年或者2019年
        """
        match = re.search(r'([12]\d{3}|\d{2})(?=[年-])', self.key)
        if match is not None:
            year = int(match.group())
            if 30 <= year < 100:
                year += 1900
            elif 0 < year < 30:
                year += 2000
            self.time.replace(year=year)

    def deal_word_year(self):
        """处理带有文字的年份

        比如：前年、去年等
        """
        word = {'大前年': -3, '前年': -2, '去年': -1, '今年': 0, '明年': 1, '次年': 1, '后年': 2, '大后年': 3}
        match = re.finditer('|'.join(word.keys()), self.key)
        for m in match:
            self.time = self.time.shift(years=word[m.group()])
