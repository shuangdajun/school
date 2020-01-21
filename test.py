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
# import datetime
# class showTime:
#     def __init__(self):
#         self.time=datetime.date.today()
#         self.haha=""
#     @property
#     def show(self):
#         return self.haha
#     @show.setter
#     def show(self,wori):
#         # self.haha=wori
#         print("pp")
#     def __repr__(self):
#         return '<user_name %r>' % self.time
#     # def __str__(self):
#     #     return '<user_name %r>' % self.time
# timer=showTime()
# timer.show="1232"
# print(timer.show)
# fdict={}
#
# with open("C:\\haha.txt","r") as f:
#     for line in f.readlines():
#         data=line.strip("\n").split("\t")
#         if data[0] not in fdict.keys():
#             fdict[data[0]]=data[1]
#         else:
#             fdict[data[0]] = fdict[data[0]]+","+data[1]
# for key,value in sorted(fdict.items()):
#     print("%s   %s"%(key,value))
#     # print("%s"%(key))



# haha={"name":"shuang"}
# ll=[1,2,3]
# def wori(**hehe):
#     print(hehe)
#
# def mm(*args):
#     print(args)
# wori(**haha)
# mm(ll)


import redis
res=redis.ConnectionPool(host="172.18.1.101",port=6379,db=2)
re=redis.Redis(connection_pool=res)
re.hmset("user_Manager",{"user":"shuangdajun"})
re.expire("user_Manager",300)