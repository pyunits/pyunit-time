#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/21 17:19
# @Author: Jtyoui@qq.com
# @Notes : 处理中文时间
from .filters import filters_string
import arrow


class Time:
    def __init__(self, current_time=None):
        self.current_time = arrow.get(current_time)

    def parse(self, string, **kwargs):
        update_time = self.current_time
        keys = filters_string(string, **kwargs)
