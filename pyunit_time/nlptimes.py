#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/12/9 10:19
# @Author: Jtyoui@qq.com
from .dateRe import DATE_RE, Solar_Holiday, Lunar_Holiday, replace, chinese_mon_number
from .timeunit import TimeUnit, TimePoint
import re
import time


class CharactersTime:
    """大型正则解析时间"""

    def __init__(self, time_base=None, prefer_future=False):
        """时间解析

        分析文件进行数据时间分析，包括复杂的时间、口语化、农历等

        :param time_base: 当前时间，格式是年-月-日 时:分:秒
        :param prefer_future: 启动预测功能
        """
        self.isPreferFuture = prefer_future
        self.pattern = re.compile(DATE_RE)
        self.timeBase = None
        self.solar_holiday = Solar_Holiday
        self.lunar_holiday = Lunar_Holiday
        self.timeBase = replace(r'\W+', '-', time_base) if time_base else time.strftime('%Y-%m-%d-%H-%M-%S')
        self.time_re = []

    def parse(self, target) -> list:
        """解析时间"""
        times = []
        input_query = self._filter(target)
        time_token = self._ex(input_query)
        for res in time_token:
            rt = res.time
            self.time_re.append(res.exp_time)
            if rt:
                times.append(rt.format("YYYY-MM-DD HH:mm:ss"))
        return times

    @staticmethod
    def _filter(word) -> str:
        """对一些不规范的表达做转换"""
        for k, v in chinese_mon_number.items():
            if k == '十':
                continue
            word = word.replace(k, v)
        pattern = re.compile("(?:周|星期)[末天日]")
        match = pattern.finditer(word)
        for m in match:
            word = word.replace(m.group(), '7')

        pattern = re.compile("[0-9]?十[0-9]?")
        match = pattern.finditer(word)
        for m in match:
            group = m.group()
            s = group.split("十")
            ten, end = int(s[0]) if s[0] else 0, int(s[1]) if s[1] else 0
            if ten == 0:
                ten = 1
            num = ten * 10 + end
            word = word.replace(m.group(), str(num))

        input_query = re.sub('\\s+|的', '', word)  # 去除不用的字
        match = re.search("[0-9]月[0-9]", input_query)
        if match is not None:
            index = input_query.find('月')
            match = re.search("[日号]", input_query[index:])
            if match is None:
                match = re.search("[0-9]月[0-9]+", input_query)
                if match is not None:
                    end = match.span()[1]
                    input_query = input_query[:end] + '号' + input_query[end:]
        match = re.search("月", input_query)
        if match is None:
            input_query = input_query.replace('个', '')
        replaces = {'中旬': '15号', '傍晚': '午后', '大年': '春节', '51': '劳动节', '白天': '早上', '：': ':', '前1天': '前天', '后1天': '后天'}
        for k, v in replaces.items():
            input_query = input_query.replace(k, v)
        return input_query

    def _ex(self, word):
        temp, start, end = [], -1, -1
        match = self.pattern.finditer(word)
        for m in match:
            start = m.start()
            if start == end:
                temp[-1] += m.group()
            else:
                temp.append(m.group())
            end = m.end()
        res = []
        context_tp = TimePoint()
        for t in temp:
            res.append(TimeUnit(t, self, context_tp))
            context_tp = res[-1].tp
        return res
