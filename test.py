#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @CharactersTime  : 2019/12/9 10:17
# @Author: Jtyoui@qq.com
from pyunit_time import CharactersTime


def test():
    """字符字符串时间解析"""
    np = CharactersTime('2019-12-19 00:00:00').parse('国庆节的前一天晚上8点半')
    print(np)  # ['2019-09-29 20:30:00']
    np = CharactersTime('2019-12-19 00:00:00').parse('今天晚上8点到明天上午10点之间')
    print(np)  # ['2019-12-19 20:00:00', '2019-12-20 10:00:00']
    np = CharactersTime('2019-12-19 00:00:00').parse('今年儿童节晚上九点一刻')
    print(np)  # ['2019-06-01 21:15:00']
    np = CharactersTime('2019-12-19 00:00:00').parse('今天中午十二点')
    print(np)  # ['2019-12-09 12:00:00']
    np = CharactersTime('2019-12-19 00:00:00').parse('明年春节')
    print(np)  # ['2020-01-25 00:00:00']
    np = CharactersTime('2019-12-19 00:00:00').parse('下下下个星期五早上7点半')
    print(np)  # ['2020-01-10 07:30:00']
    np = CharactersTime('2019-12-19 00:00:00').parse('今年的大寒')
    print(np)  # ['2020-01-20 00:00:00']
    np = CharactersTime('2019-12-19 00:00:00').parse('189号')
    print(np)  # []


if __name__ == '__main__':
    test()
