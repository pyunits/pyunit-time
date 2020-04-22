# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:47
# @Author: Jtyoui@qq.com
# @Notes : 处理星期
from pyunit_gof import IObserver
import re


class Weeks(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.set_number_week()
        self.week_fth()
        self.set_shift_week()
        return self.time

    def set_number_week(self):
        """设置星期
        比如： 一个星期以前
        """
        rule = r'(\d+)个?(周|星期|礼拜)[以之]?[前后]'
        match = re.search(rule, self.key)
        if match:
            week = int(match.group(1))
            week = -week if '前' in self.key else week
            self.time = self.time.shift(weeks=week)

    def set_shift_week(self):
        """替换日期
        比如： 上个星期6、上两个星期3
        """
        rule = r'([上下]+)(\d+)?个?(?:周|星期)([1-7天日]?)'
        match = re.search(rule, self.key)
        current_week = self.time.isoweekday()
        if match:
            count = match.group(1)  # 表示有多少个 上上
            number = match.group(2)  # 表示多少次数
            day = match.group(3)
            counts = -len(count) if '上' in count else len(count)
            if number and int(number) > 1:
                counts = -int(number) if '上' in count else int(number)
            if day:
                if day.isdigit():
                    days = int(day) - current_week
                else:
                    days = 7 - current_week
            else:
                days = 0
            self.time = self.time.shift(weeks=counts, days=days)
        else:
            rule = r'(?:周|星期|礼拜)([1-7天日]?)'
            match = re.search(rule, self.key)
            if match:
                day = match.group(1)
                if day.isdigit():
                    days = int(day) - current_week
                else:
                    days = 7 - current_week
                self.time = self.time.shift(days=days)

    def week_fth(self):
        """处理x个月第几个星期之类的问题

        比如： 第1个星期2
        """
        rule = '第([1-5])个?(?:周|星期|礼拜)([1-7天日])'
        match = re.search(rule, self.key)
        if match:
            fth = int(match.group(1))
            day = match.group(2)
            if not day.isdigit():
                day = 7
            else:
                day = int(day)
            self.time = self.time.replace(day=1)
            if day == self.time.isoweekday():
                fth -= 1
                self.time = self.time.shift(weeks=fth)
            else:
                days = self.time.isoweekday() - day
                self.time = self.time.shift(weeks=fth, days=days)
