#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/5/9 11:50
# @Author: Jtyoui@qq.com
from .CTC_ import CTC  # 农历转阳历
from .LSC import LunarDate, SolarDate, LunarSolarDateConverter  # 阴历和阳历转换
from .SC_ import SC  # 阳历转农历
from .batchcalendar import BatchCalendar  # 批量转换日历

__version__ = '2020.06.02'
__author__ = 'Jtyoui'
__description__ = '常见的日历转换器'
__email__ = 'jtyoui@qq.com'
__names__ = 'pyUnit_calendar'
__url__ = 'https://github.com/PyUnit/pyunit-calendar'
