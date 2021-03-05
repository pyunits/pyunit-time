#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/3/11 9:59
# @Author: Jtyoui@qq.com
"""观察者模式
观察者模式是一种对象行为模式。它定义对象间的一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都得到通知并被自动更新。
在观察者模式中，主题是通知的发布者，它发出通知时并不需要知道谁是它的观察者，可以有任意数目的观察者订阅并接收通知。
观察者模式不仅被广泛应用于软件界面元素之间的交互，在业务对象之间的交互、权限管理等方面也有广泛的应用。
"""
from abc import ABCMeta, abstractmethod


class IObserver(metaclass=ABCMeta):
    __doc__ = """观察者的抽象类,具体实现"""

    @abstractmethod
    def notify(self, observable, *args, **kwargs):
        """通知观察者对象

        :param observable: 观察者具体的实现方法
        """
        pass


class IObservable(metaclass=ABCMeta):
    __doc__ = """可观察者对象"""

    @abstractmethod
    def __init__(self):
        self.observers = []

    @abstractmethod
    def subscribe(self, observer: IObserver):
        """订阅观察者

        :param observer: 观察者对象。是一个class对象
        """
        pass

    @abstractmethod
    def unsubscribe(self, observer: IObserver):
        """退订观察者

        :param observer: 观察者对象。是一个class对象
        """
        pass

    @abstractmethod
    def notify(self, *args, **kwargs):
        """通知观察者对象:一般都是遍历通知

        >>> for o in self.observers: pass

        """
        pass
