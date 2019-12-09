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
import openpyxl
from openpyxl import load_workbook
load_workbook('C:\\flask-school-app-and-api-master\\app\\upload\\Students_info.xlsx')