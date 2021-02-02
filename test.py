#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/12/9 10:17
# @Author: Jtyoui@qq.com
from pyunit_time import Time


def time():
    """字符字符串时间解析"""
    assert Time('2020-4-22 00:00:00').parse('这个月的第三个星期天') == [
        {'key': '这个月第3个星期天', 'keyDate': '2020-04-19 00:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('前2年的国庆节的后一天晚上8点半') == [
        {'key': '前2年国庆节后1天晚上8点半', 'keyDate': '2018-09-30 20:30:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('上上个月') == [
        {'key': '上上个月', 'keyDate': '2020-02-22 00:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('今天晚上8点') == [
        {'key': '今天晚上8点', 'keyDate': '2020-04-22 20:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('今年儿童节晚上九点一刻') == [
        {'key': '今年儿童节晚上9点1刻', 'keyDate': '2020-06-01 21:15:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('今天中午十二点') == [
        {'key': '今天中午12点', 'keyDate': '2020-04-22 12:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('明年春节') == [
        {'key': '明年春节', 'keyDate': '2021-02-12 00:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('明年的感恩节') == [
        {'key': '明年感恩节', 'keyDate': '2021-11-25 00:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('下3个星期1早上7点半') == [
        {'key': '下3个星期1早上7点半', 'keyDate': '2020-05-11 07:30:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('今年的大寒') == [
        {'key': '今年大寒', 'keyDate': '2021-01-20 00:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('2019年12月') == [
        {'key': '2019年12月', 'keyDate': '2019-12-01 00:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('8年前') == [
        {'key': '8年前', 'keyDate': '2012-04-22 00:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('三天以后') == [
        {'key': '3天以后', 'keyDate': '2020-04-25 00:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('三天之内的下午3点') == [
        {'key': '3天之内下午3点', 'keyDate': '2020-04-25 15:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('后三天的下午4点56秒') == [
        {'key': '后3天下午4点56秒', 'keyDate': '2020-04-25 16:00:56', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('2020-1-2 10:20:10') == [
        {'key': '2020-1-2 10:20:10', 'keyDate': '2020-01-02 10:20:10', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('明晚九点，明天晚上九点') == [
        {'key': '明晚9点', 'keyDate': '2020-04-23 21:00:00', 'baseDate': '2020-04-22 00:00:00'},
        {'key': '明天晚上9点', 'keyDate': '2020-04-23 21:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 00:00:00').parse('昨晚九点，明天晚上九点') == [
        {'key': '昨晚9点', 'keyDate': '2020-04-21 21:00:00', 'baseDate': '2020-04-22 00:00:00'},
        {'key': '明天晚上9点', 'keyDate': '2020-04-23 21:00:00', 'baseDate': '2020-04-22 00:00:00'}]

    assert Time('2020-4-22 10:10:10').parse('我后天去北京') == [
        {'key': '后天', 'keyDate': '2020-04-24 10:10:10', 'baseDate': '2020-04-22 10:10:10'}]

    assert Time('2020-9-20 10:10:10').parse('00年出生的孩子爱看的电视剧') == [
        {'key': '00年', 'keyDate': '2000-09-20 10:10:10', 'baseDate': '2020-09-20 10:10:10'}]

    assert Time('2020-9-20 10:10:10').parse('这个月的最后一天的前一天') == [
        {'key': '这个月最后1天前1天', 'keyDate': '2020-09-29 10:10:10', 'baseDate': '2020-09-20 10:10:10'}]

    assert Time('2020-9-20 10:10:10').parse('这个月的第一天') == [
        {'key': '这个月第1天', 'keyDate': '2020-09-01 10:10:10', 'baseDate': '2020-09-20 10:10:10'}]

    assert Time('2020-9-20 10:10:10').parse('这个月的最后1个星期5') == [
        {'key': '这个月最后1个星期5', 'keyDate': '2020-09-25 10:10:10', 'baseDate': '2020-09-20 10:10:10'}]

    assert Time('2020-9-20 10:10:10').parse('这个月的第1个星期1') == [
        {'key': '这个月第1个星期1', 'keyDate': '2020-09-07 10:10:10', 'baseDate': '2020-09-20 10:10:10'}]

    assert Time('2020-9-20 10:10:10').parse('一个小时前') == [
        {'key': '1个小时前', 'keyDate': '2020-09-20 09:10:10', 'baseDate': '2020-09-20 10:10:10'}]

    assert Time('2020-9-20 10:10:10').parse('再过8小时') == [
        {'key': '再过8小时', 'keyDate': '2020-09-20 18:10:10', 'baseDate': '2020-09-20 10:10:10'}]


if __name__ == '__main__':
    time()
