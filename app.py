# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/5/7 上午11:27
# @Author: Jtyoui@qq.com
# @Notes :  flask 启动
import json

from flask import Flask, jsonify, request

from pyunit_time import Time

app = Flask(__name__)


def flask_content_type(requests):
    """根据不同的content_type来解析数据"""
    if requests.method == 'POST':
        if 'application/x-www-form-urlencoded' in requests.content_type:
            data = requests.form
        elif 'application/json' in requests.content_type:
            data = requests.json
        else:  # 无法被解析出来的数据
            data = json.loads(requests.data)
        return data
    elif requests.method == 'GET':
        return requests.args


@app.route('/pyunit/time', methods=['POST', 'GET'])
def py_time():
    try:
        data = flask_content_type(request)
        current_time = data.get('current_time', None)
        format_ = data.get('format', 'YYYY-MM-DD HH:mm:ss')
        string = data.get('string', '')
        time = Time(current_time=current_time, format_=format_).parse(string=string)
        return jsonify(code=200, result=time)
    except Exception as e:
        return jsonify(code=500, error=str(e))
