# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:44
# @Author: Jtyoui@qq.com
# @Notes : 处理阳历的节日
from pyunit_gof import IObserver
import re


def solar_holiday_to_number(string) -> str:
    """将阳历的节日转为具体的某月某日

    比如： 国庆节 -> 10月1日

    :param string: 带有阳历节日的数据
    :return: 转为具体的日期
    """
    solar = {
        "元旦节": "1月1日",
        "情人节": "2月14日",
        "湿地日": "2月2日",
        "妇女节": "3月8日",
        "植树节": "3月12日",
        "世界水日": "3月22日",
        "愚人节": "4月1日",
        "地球日": "4月22日",
        "海军节": '4月23日',
        "劳动节": "5月1日",
        "五四青年节": "5月4日",
        "青年节": "5月4日",
        "护士节": "5月12日",
        "博物馆日": "5月18日",
        "旅游日": "5月19日",
        "儿童节": "6月1日",
        "建党节": "7月1日",
        "航海节": "7月11日",
        "建军节": "8月1日",
        "教师节": "9月10日",
        "国耻日": "9月18日",
        "国庆节": "10月1日",
        "记者节": "11月8日",
        "学生日": "11月17日",
        "艾滋病日": "12月1日",
        "宪法日": "12月4日",
        "平安夜": "12月24日",
        "圣诞节": "12月25日",
    }
    solar_holiday = '|'.join(solar.keys())
    result = re.sub(pattern=solar_holiday, repl=lambda x: solar[x.group()], string=string)
    return result


class SolarHoliday(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.key = solar_holiday_to_number(self.key)
        self.deal_mon_day()
        return self.time

    def deal_mon_day(self):
        """处理月和日"""
        match = re.search(r'(\d+)月(\d+)日', self.key)
        if match:
            mon = int(match.group(1))
            day = int(match.group(2))
            self.time = self.time.replace(month=mon, day=day)
