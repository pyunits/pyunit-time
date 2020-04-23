#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/20 16:28
# @Author: Jtyoui@qq.com
# @Notes : 解析正则表达式，过滤无效成分，分析出哪些是时间关键词
import re
import os

txt = os.path.dirname(__file__) + os.sep + 're.txt'
TIME_RE = '|'.join([i.strip() for i in open(txt, encoding='utf-8')])
pattern = re.compile(TIME_RE)


def get_time_key(string) -> list:
    """根据字符串提取字符串中的时间关键词

    比例： 国庆节的前一天晚上8点半
    返回： ['国庆节', '前一天晚上8点半']

    :param string: 关于口述话的时间字符串
    :return: 时间关键词
    """
    keys, start, end = [], -1, -1
    match = pattern.finditer(string)
    for key in match:
        start = key.start()
        if start == end:
            keys[-1] += key.group()
        else:
            keys.append(key.group())
        end = key.end()
    return keys


def ten_to_number(string: str) -> str:
    """关于中文的十的转换为阿拉伯数字

    中文中的十比较特殊，转换格式分为四种

    1、十点     ： 这里的十转为数字是 10点
    2、一十三点 ：这里的十不转化。直接是： 13点
    3、十三点   : 这里的十转为1，表示：13点
    4、一十点   ： 这里的十转为0，表示10点。

    :param string: 对中文中的十进行数字化处理
    :return: 处理后的阿拉伯数字
    """
    temporary = []
    ten = {
        '一': '1',
        '二': '2',
        '两': '2',
        '三': '3',
        '四': '4',
        '五': '5',
        '六': '6',
        '七': '7',
        '八': '8',
        '九': '9'
    }
    for index, char in enumerate(string):
        if char == '十':
            if (index == 0) or (not ten.get(string[index - 1])):  # 第一个字符是十或者十前面一个不是数字，那么就只能有两种情况
                if index != len(string) - 1:  # 如果当前是最后一个字符，那么该十没有任何含义
                    if ten.get(string[index + 1]):  # 后面有一个数字,那么这里的十就充当了 1,否则就充当了 10
                        temporary.append('1')
                    else:
                        temporary.append('10')
            else:  # 十前面一个字符是数字，那么就只能有两种情况
                if index != len(string) - 1:  # 如果当前是最后一个字符，那么该十没有任何含义
                    if ten.get(string[index + 1]):  # 如果后面一个是数字，那么十什么也不充当,否则就充当了 0
                        pass
                    else:
                        temporary.append('0')
        else:
            temporary.append(ten.get(char, char))
    return ''.join(temporary)


def solar_mon_to_num(string) -> str:
    """中文中的阳历月份进行转为阿拉伯数字

    切记：下面是阳历的月份，不是农历的月份

    :param string: 将阳历的月份转为阿拉伯数字
    :return: 转换完毕的阿拉伯数字
    """
    solar = {
        '一月': '1月',
        '二月': '2月',
        '两月': '2月',
        '三月': '3月',
        '四月': '4月',
        '五月': '5月',
        '六月': '6月',
        '七月': '7月',
        '八月': '8月',
        '九月': '9月',
        '一十月': '10月',
        '一十一月': '11月',
        '一十二月': '12月',
        '十月': '10月',
        '十一月': '11月',
        '十二月': '12月',
    }
    solar_re = '|'.join(solar.keys())
    result = re.sub(pattern=solar_re, repl=lambda x: solar[x.group()], string=string)
    return result


def remove_conjunctions(string, remove_symbol=False, remove_re=None) -> str:
    """
    去除时间的连接词


    比如： 国庆节的前一天。这里的实际充当了连词
          国庆节，前一天。这里的，可以去掉

    :param string: 过滤字符串
    :param remove_symbol: 如果为真。过滤全部符号，如果为假，不过滤。
    :param remove_re: 自定义移除正则
    :return: 过滤后的字符串
    """
    if remove_re:
        match = remove_re
        return re.sub(match, '', string)
    else:
        string = string.replace('的', '').replace('：', ':')
        rule = r'(\d+-\d+(-\d+)?)|(\d+\.\d+(\.\d+)?)|(\d+/\d+(/\d+)?)|\d+:\d+(:\d+)?'
        if not re.search(rule, string):
            string = re.sub(r'\s+', '', string)
    if remove_symbol:
        string = re.sub(r'\s+', '', string)
    return string


def symbol_replace(string):
    """符号替换"""
    symbol = {
        '：': ':',
    }
    result = re.sub(pattern='|'.join(symbol.keys()), repl=lambda x: symbol[x.group()], string=string)
    return result


def filters_string(string, **kwargs):
    """进行初始化过滤"""
    remove_symbol = kwargs.get('remove_symbol', False)
    remove_re = kwargs.get('remove_re', None)
    string = symbol_replace(string)  # 符号替换
    string = remove_conjunctions(string, remove_symbol, remove_re)  # 去除时间的连接词
    string = solar_mon_to_num(string)  # 中文中的阳历月份进行转为阿拉伯数字
    string = ten_to_number(string)  # 关于中文的十的转换为阿拉伯数字
    keys = get_time_key(string)  # 根据字符串提取字符串中的时间关键词
    return keys
