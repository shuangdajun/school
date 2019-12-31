# # def test1():
# #     '''test1...'''
# #     print('test1')
# #
# # def test2():
# #     '''test2...'''
# #     print('test2')
# #
# #
# # print (test1.__doc__)
# # print (test1.__name__)
# # print (test2.__doc__)
# # print (test2.__name__)
#
#
# # coding:utf8
# from functools import wraps
#
# def login_required(view_func):
#     """hehe"""
#     def wrapper(*args,**kwargs):
#         """haha"""
#         pass
#     return wrapper
#
# @login_required
# def test1():
#     '''test1...'''
#     print('test1')
#
# @login_required
# def test2():
#     '''test2...'''
#     print('test2')
#
#
# print (test1.__doc__)
# print (test1.__name__)
# print (test2.__doc__)
# print (test2.__name__)
#
#
#
# # coding:utf8
# # from functools import wraps
# #
# # def login_required(view_func):
# #     @wraps(view_func)
# #     def wrapper(*args,**kwargs):
# #         pass
# #     return wrapper
# #
# # @login_required
# # def test1():
# #     '''test1...'''
# #     print('test1')
# #
# # @login_required
# # def test2():
# #     '''test2...'''
# #     print('test2')
# #
# # print (test1.__name__)
# # print (test1.__doc__)
#
# print (test2.__name__)
# print (test2.__doc__)
#


# !/usr/bin/env python
# -*- coding:utf-8 -*-
# from celery import Celery
#
# from config.config import CeleryConfig
#
# app = Celery("haha")
# app.config_from_object(CeleryConfig)
# #app.config_from_object(CeleryConfig)  # 指定配置文件
#
#
# @app.task(bind=True)
# def taskA(self,x, y):
#     return x + y,self.id

#
# @app.task
# def taskB(x, y, z):
#     return x + y + z
#
#
# @app.task
# def add(x, y):
#     return x-y
import datetime
class showTime:
    def __init__(self):
        self.time=datetime.date.today()
        self.haha=""
    @property
    def show(self):
        return self.haha
    @show.setter
    def show(self,wori):
        # self.haha=wori
        print("pp")
    def __repr__(self):
        return '<user_name %r>' % self.time
    # def __str__(self):
    #     return '<user_name %r>' % self.time
timer=showTime()
timer.show="1232"
print(timer.show)
