#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/12/9 10:17
# @Author: Jtyoui@qq.com
import json
import os.path
import unittest

from pyunit_time import Time


def load_json() -> list:
    place = os.path.dirname(__file__)
    test_file = os.path.join(place, "test.json")
    with open(test_file, encoding="utf8") as fp:
        return json.load(fp)


class MyTestCase(unittest.TestCase):
    def test_time(self):
        tests = load_json()
        for text in tests:
            input_ = text["input"]
            truth = text["output"]
            base_time = truth[0]["baseDate"]
            predict = Time(base_time).parse(input_)

            self.assertEqual(predict, truth)


if __name__ == "__main__":
    unittest.main()
