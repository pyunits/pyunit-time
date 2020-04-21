#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/21 16:24
# @Author: Jtyoui@qq.com
# @Notes : 关于特殊节日的计算法则
from pyunit_time.holiday import easter_holiday
import re


def special_holiday_calculation(string) -> str:
    """关于特殊节日的计算法则

    比如： 计算复活节， 每年过春分月圆后的第一个星期天

    :param string: 包含特殊节日
    :return: 转为具体的年月日
    """
    special_holiday = '复活节|'
    result = re.sub(pattern=special_holiday, repl=lambda x: easter_holiday(x.group()), string=string)
    return result
