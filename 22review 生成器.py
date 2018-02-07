# -*- coding:utf-8 -*-


def func(a):
    return a

def hello():
    yield func(1) #挂起函数，并且返回右面表达式的值给等号左面的变量
    print "继续执行１"
    yield func(2)
    print "继续执行２"
    yield func(3)

a = hello()
# 生成器本身也是一种特殊的迭代器
aa = next(a)
bb = next(a)
print next(a)
print next(a)
# print next(a)
# print next(a)


