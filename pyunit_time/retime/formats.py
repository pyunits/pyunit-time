#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/23 13:59
# @Author: Jtyoui@qq.com
# @Notes : 处理格式化字符串
from ..observer import IObserver
import arrow
import re


class Formats(IObserver):
    def __init__(self):
        self.key = None
        self.time = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        self.set_replace_format()
        return self.time

    def set_replace_format(self):
        """处理格式化字符串
        比如：2020-02-02、2020.02.02、2020/02/02等格式
        """
        rule = r'(\d+-\d+(-\d+)?)|(\d+\.\d+(\.\d+)?)|(\d+/\d+(/\d+)?)'
        match = re.search(rule, self.key)
        if match:
            if match.lastindex == 1:
                f = '-'
            elif match.lastindex == 3:
                f = '.'
            else:
                f = '/'
            try:
                group = match.group().split(f)
                if len(group) >= 1 and 1000 < int(group[0]) < 3000:  # 判断年
                    if len(group) >= 2 and 0 < int(group[1]) <= 12:  # 判断月
                        if len(group) == 3 and 0 < int(group[2]) <= 31:  # 判断日。可以不存在
                            data = match.group()
                        else:
                            data = F'{group[0]}-{group[1]:0>2}'
                        self.time = arrow.get(data)
            except arrow.parser.ParserError:
                pass
        rule = r'\d+:\d+(:\d+)?'
        match = re.search(rule, self.key)
        if match:
            h = match.group().split(':')
            if len(h) == 2:
                self.time = self.time.replace(hour=int(h[0]), minute=int(h[1]))
            else:
                self.time = self.time.replace(hour=int(h[0]), minute=int(h[1]), second=int(h[2]))
