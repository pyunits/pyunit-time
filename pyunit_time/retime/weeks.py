# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:47
# @Author: Jtyoui@qq.com
# @Notes : 处理星期
import re

from ..observer import IObserver


class Weeks(IObserver):
    def __init__(self):
        self.key = None
        self.time = None
        self.future = None
        self.final = False  # 增加最终属性，如果是 True，表示该属性已经是最终结果，不在继续判断

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.future = observable.is_future
        self.set_number_week()
        self.week_fth()
        self.set_shift_week()
        return self.time

    def future_week(self, day, current):
        """处理超过了当前的星期，比如：今天是星期四，问星期三，那么星期三应当为未来时间，即下周星期三
        answer week over the current week,eg: answer Wednesday, today Thursday. answer Wednesday is next Week Wednesday
        """
        flag_day = day.isdigit()
        if flag_day:
            int_day = int(day)
            if self.future:
                if int_day < current:  # 当前日期超过了询问的日期
                    days = int_day + 7 - current
                    return days
            days = int_day - current
        else:
            if self.future and current == 7:
                days = 7
            else:
                days = 7 - current
        return days

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
            if match and (not self.final):  # 替换星期和 week_fth 有重复的可能，需要判断是否不在继续替换
                day = match.group(1)
                days = self.future_week(day, current_week)
                self.time = self.time.shift(days=days)

    def week_fth(self):
        """处理x个月第几个星期之类的问题

        比如： 第1个星期2
        """
        rule = '(?<=[第最后])([1-5])个?(?:周|星期|礼拜)([1-7天日])'
        match = re.search(rule, self.key)
        if match:
            fth = int(match.group(1))  # 替换x个周
            day = match.group(2)  # 获取星期x
            day = 7 if not day.isdigit() else int(day)

            if '最后' in self.key:
                self.time = self.time.shift(months=1)

            self.time = self.time.replace(day=1)  # 更改时间为当月第一天
            current_week = self.time.isoweekday()  # 获取当月第一天是星期几

            # 如果当前星期刚好是当月第一天，那么替换的周数少一
            several_days = day - current_week  # 还差多少天就是星期x
            self.time = self.time.shift(days=several_days)

            if '第' in self.key:  # 这个是往前推
                fth -= 1 if several_days >= 0 else 0
                self.time = self.time.shift(weeks=fth)
            else:  # 这个是往后推
                fth -= 0 if several_days >= 0 else 1
                self.time = self.time.shift(weeks=-fth)

            self.final = True
