# -*- coding:utf-8
import functools
def log(permission):
    def hehe(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            print('call %s():' % func.__name__)
            print('args = {}'.format(*args))
            return func(*args,**kwargs)
        return wrapper
    return hehe


@log(1001)
def test(p):
    print(test.__name__ + " param: " + p)

test("I'm a param")