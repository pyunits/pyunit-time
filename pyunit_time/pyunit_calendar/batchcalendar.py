#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/5/10 9:15
# @Author: Jtyoui@qq.com
"""利用文本数据进行日历转换,转换只能是日期

该方法属于大量日期转化。消耗内存为代价提高速度。该类只能查询1901-2099年。如果还需要查询更久,请查看文件格式: https://github.com/PyUnit/pyunit-calendar/releases
根据改格式修改并且压缩成zip,修改文件的路径,使用环境变量中的地址,环境变量名是:CALENDER_PATH.
"""
import os
import zipfile


class BatchCalendar:

    def __init__(self, load_date_file=None):
        """初始化
        配置批量日历文件地址,优先使用环境变量中的地址,环境变量名是:CALENDER_PATH,没有就使用默认的文件地址
        最新的日历文件地址是: https://github.com/PyUnit/pyunit-calendar/releases
        :param load_date_file: 日历文件地址
        :return: 农历,天干地支,阳历
        """
        self.LunarCalendar = {}  # 阴历
        self.HSTTB = {}  # 天干地支
        self.SolarCalendar = {}  # 阳历
        if load_date_file and os.path.exists(load_date_file):
            path = load_date_file
        else:
            path = os.environ['CALENDER_PATH'] if os.environ.get('CALENDER_PATH') else os.path.dirname(
                __file__) + os.sep + 'date.zip'
        uz = self._unzip(path, 'date.txt')
        ls = uz.split('\r\n')
        for line in ls[:-1]:
            ct, cs, td = line.split('\t')
            self.LunarCalendar[ct] = cs
            self.SolarCalendar[cs] = ct
            if self.HSTTB.get(td):
                self.HSTTB[td].append(ct)
            else:
                self.HSTTB[td] = [ct]

    @staticmethod
    def _unzip(zip_address, file_name, encoding='UTF-8'):
        """解压zip数据包

        :param zip_address: 压缩包的地址
        :param file_name: 压缩包里面文件的名字
        :param encoding: 文件的编码
        :return: 压缩包里面的数据：默认编码的UTF-8
        """
        f = zipfile.ZipFile(zip_address)
        fp = f.read(file_name)
        lines = fp.decode(encoding)
        return lines

    def td_to_ctc(self, td):
        """天干地支纪年转农历

        :param td: 输入一个天干地支纪年
        :return: 农历
        """
        return self.HSTTB.get(td)

    def td_to_sc(self, td):
        """天干地支纪年转阳历

        :param td: 输入一个天干地支纪年
        :return: 阳历
        """
        ctc = self.td_to_ctc(td)
        return [self.ctc_to_sc(c) for c in ctc]

    def ctc_to_sc(self, ctc):
        """农历转阳历

        :param ctc: 农历
        :return: 阳历
        """
        return self.LunarCalendar.get(ctc)

    def ctc_to_td(self, ctc):
        """农历转天干地支

        :param ctc: 农历
        :return: 天干地支,找不到返回空
        """
        for td_, ctc_ in self.HSTTB.items():
            if ctc in ctc_:
                return td_
        return ''

    def sc_to_ctc(self, sc):
        """阳历转农历

        :param sc: 阳历
        :return: 农历
        """
        return self.SolarCalendar.get(sc)

    def sc_to_td(self, sc):
        """阳历转天干地支纪年

        :param sc: 阳历
        :return: 天干地支纪年
        """
        ctc = self.sc_to_ctc(sc)
        return self.ctc_to_td(ctc)
