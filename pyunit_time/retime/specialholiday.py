#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/21 16:24
# @Author: Jtyoui@qq.com
# @Notes : 关于特殊节日的计算法则
from ..observer import IObserver
import arrow
import math
import re


def easter_holiday(year: [int, str]) -> str:
    """关于复活节的月份日计算

    每年过春分月圆后的第一个星期天
    该算法年份只限于1900年到2099年

    :param year: 那一年，比如：2020
    :return: 返回该年的复活节年月日 : 2020年4月12日
    """
    year = int(year)
    if 1900 < year < 2099:
        n = year - 1900
        a = n % 19
        q = math.floor(n / 4)
        b = math.floor((7 * a + 1) / 19)
        m = (11 * a + 4 - b) % 29
        w = (n + q + 31 - m) % 7
        d = 25 - m - w
        if d > 0:
            mon = 4
        else:
            mon = 3
            d += 31
        return F'{year}-{mon}-{d}'
    else:
        raise ValueError('该算法年份只限于1900年到2099年')


def mother_day(year: [int, str]) -> str:
    """关于母亲节的月份日计算

    公历5月第2个周日是母亲节

    :param year: 那一年，比如：2020
    :return: 返回该年的母亲节年月日 ：2020年5月10日
    """
    five = F'{year}-05-01'
    date = arrow.get(five)
    week = date.isoweekday()
    mother = date.shift(days=14 - week)
    return F'{mother.year}-{mother.month}-{mother.day}'


def father_day(year: [int, str]) -> str:
    """关于父亲节的月份日计算

    公历6月第3个周日是父亲节

    :param year: 那一年，比如：2020
    :return: 返回该年的父亲节年月日 ：2020年6月21日
    """
    six = F'{year}-06-01'
    date = arrow.get(six)
    week = date.isoweekday()
    mother = date.shift(days=21 - week)
    return F'{mother.year}-{mother.month}-{mother.day}'


def thanksgiving(year: [int, str]) -> str:
    """关于感恩节的月份日计算

    公历11月第4个周四是感恩节

    :param year: 那一年，比如：2020
    :return: 返回该年的感恩节年月日 ：
    """
    eleven = F'{year}-11-01'
    date = arrow.get(eleven)
    week = date.isoweekday()
    day = (25 - week) if (4 - week) >= 0 else (32 - week)
    mother = date.shift(days=day)
    return F'{mother.year}-{mother.month}-{mother.day}'


class SpecialHoliday(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.special_holiday_calculation()
        return self.time

    def special_holiday_calculation(self):
        """关于特殊节日的计算法则

        比如： 计算复活节， 每年过春分月圆后的第一个星期天

        """
        special = {
            '复活节': easter_holiday,
            '母亲节': mother_day,
            '父亲节': father_day,
            '感恩节': thanksgiving,
        }
        match = re.search('|'.join(special.keys()), self.key)
        if match:
            fun = special[match.group()]
            date = fun(self.time.year)
            year, mon, day = date.split('-')
            self.time = self.time.replace(year=int(year), month=int(mon), day=int(day))
