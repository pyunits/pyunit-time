# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:46
# @Author: Jtyoui@qq.com
# @Notes : 处理24时节
from ..observer import IObserver
import re


def china_24(year: int, china_st: str):
    """二十世纪和二十一世纪，24节气计算"""
    if (19 == year // 100) or (2000 == year):
        st_key = [6.11, 20.84, 4.6295, 19.4599, 6.3826, 21.4155, 5.59, 20.888, 6.318, 21.86, 6.5, 22.2, 7.928, 23.65,
                  8.35, 23.95, 8.44, 23.822, 9.098, 24.218, 8.218, 23.08, 7.9, 22.6]
    else:
        st_key = [5.4055, 20.12, 3.87, 18.73, 5.63, 20.646, 4.81, 20.1, 5.52, 21.04, 5.678, 21.37, 7.108, 22.83, 7.5,
                  23.13, 7.646, 23.042, 8.318, 23.438, 7.438, 22.36, 7.18, 21.94]
    solar_terms = {
        '小寒': [st_key[0], '1', (2019, -1), (1982, 1)],
        '大寒': [st_key[1], '1', (2082, 1)],
        '立春': [st_key[2], '2', (None, 0)],
        '雨水': [st_key[3], '2', (2026, -1)],
        '惊蛰': [st_key[4], '3', (None, 0)],
        '春分': [st_key[5], '3', (2084, 1)],
        '清明': [st_key[6], '4', (None, 0)],
        '谷雨': [st_key[7], '4', (None, 0)],
        '立夏': [st_key[8], '5', (1911, 1)],
        '小满': [st_key[9], '5', (2008, 1)],
        '芒种': [st_key[10], '6', (1902, 1)],
        '夏至': [st_key[11], '6', (None, 0)],
        '小暑': [st_key[12], '7', (2016, 1), (1925, 1)],
        '大暑': [st_key[13], '7', (1922, 1)],
        '立秋': [st_key[14], '8', (2002, 1)],
        '处暑': [st_key[15], '8', (None, 0)],
        '白露': [st_key[16], '9', (1927, 1)],
        '秋分': [st_key[17], '9', (None, 0)],
        '寒露': [st_key[18], '10', (2088, 0)],
        '霜降': [st_key[19], '10', (2089, 1)],
        '立冬': [st_key[20], '11', (2089, 1)],
        '小雪': [st_key[21], '11', (1978, 0)],
        '大雪': [st_key[22], '12', (1954, 1)],
        '冬至': [st_key[23], '12', (2021, -1), (1918, -1)]
    }
    if china_st in ['小寒', '大寒', '立春', '雨水']:
        flag_day = int((year % 100) * 0.2422 + solar_terms[china_st][0]) - int((year % 100 - 1) / 4)
    else:
        flag_day = int((year % 100) * 0.2422 + solar_terms[china_st][0]) - int((year % 100) / 4)
    # 特殊年份处理
    for special in solar_terms[china_st][2:]:
        if year == special[0]:
            flag_day += special[1]
            break
    if china_st in ['小寒', '大寒']:
        year += 1
    return year, solar_terms[china_st][1], flag_day


class SolarTerm24(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.set_24()
        return self.time

    def set_24(self):
        """设置中国的24节气"""
        rule = '小寒|大寒|立春|雨水|惊蛰|春分|清明|谷雨|立夏|小满|芒种|夏至|小暑|大暑|立秋|处暑|白露|秋分|寒露|霜降|立冬|小雪|大雪|冬至'
        match = re.search(rule, self.key)
        if match:
            year, mon, day = china_24(self.time.year, match.group())
            self.time = self.time.replace(year=year, month=int(mon), day=day)
