# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/5/7 上午11:27
# @Author: Jtyoui@qq.com
# @Notes :  restful 启动
from fastapi import FastAPI, Query
from pyunit_time import Time
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title='时间抽取', description='基于规则抽取、时间抽取接口文档', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResponseModal(BaseModel):
    """返回格式类型"""
    msg: str = 'success'
    code: int = 200
    result: list = [
        {
            "baseDate": "获取文本认为的开始时间",
            "key": "时间关键字",
            "keyDate": "关键字分析出的时间"
        }
    ]


@app.get('/pyunit/time', summary='时间提取接口', response_model=ResponseModal)
def py_time(current_time: str = Query(None, description='填写你认为的开始时间',
                                      regex=r'[1-9]\d{3}-([0-9]|1[0-2])-([0-9]|[1-2][0-9]|3[0-1]) \d{1,2}:\d{1,2}:\d{1,2}',
                                      title='2020-4-22 00:00:00'),
            data: str = Query(..., description='输入要分析的语句', title='一个小时前')):
    try:
        time = Time(current_time=current_time, format_='YYYY-MM-DD HH:mm:ss').parse(string=data)
        return ResponseModal(result=time)
    except Exception as e:
        return ResponseModal(msg=str(e), code=0)
