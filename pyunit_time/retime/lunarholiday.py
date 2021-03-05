# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:44
# @Author: Jtyoui@qq.com
# @Notes : 处理农历的节日
from ..observer import IObserver
from ..pyunit_calendar import LunarSolarDateConverter, LunarDate
import re

Lunar_Holiday = {
    "春节": "01-01",
    "元宵": "01-15",
    "中和": "02-02",
    '龙头节': "02-02",
    "端午": "05-05",
    "7夕": "07-07",
    "中元": "07-15",
    "中秋": "08-15",
    "重阳": "09-09",
    '寒衣节': '10-1',
    '下元节': '10-15',
    '腊八节': '12-08',
    '除夕': '12-30'
}


class LunarHoliday(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.set_lunar_holiday()
        return self.time

    def set_lunar_holiday(self):
        match = re.search('|'.join(Lunar_Holiday.keys()), self.key)
        if match:
            mon, day = Lunar_Holiday[match.group()].split('-')
            ls_converter = LunarSolarDateConverter()
            lunar = LunarDate(self.time.year, int(mon), int(day))
            solar = ls_converter.lunar_to_solar(lunar)
            self.time = self.time.replace(year=solar.solarYear, month=solar.solarMonth, day=solar.solarDay)
