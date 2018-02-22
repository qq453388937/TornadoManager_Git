# -*- coding:utf-8 -*-
# 生成器，要数据的时候返回数据，不要数据的时候不返回是生成器的特征

# python 3 中可以用return 返回一个值，
# python 2 中只能return 不能返回值

"""
for...in...循环的本质
for item in Iterable 循环的本质就是先通过iter()函数获取可迭代对象Iterable的迭代器，
然后对获取到的迭代器不断调用next()方法来获取下一个值并将其赋值给item，当遇到StopIteration的异常后循环结束。
"""

# list = [x for x in range(100)] # 列表推导式
# a = (x for x in range(100))  # 生成器表达式,a 是生成器对象，特殊的迭代器，可以用for 循环操作
# for x in a:
#     print x

# 生成器
import time


class Person:
    def __init__(self, name):
        self.name = name


def Fib(n):  # n代表求从0开始第n个 斐波那契数列的值  n > 0 才有值
    """生成器需要调用才能产生生成器对象，生成器对象才能next
     f = Fib(10)
     next(f)
     next(f)  == send(None)
    """
    index = 0
    num1, num2 = 0, 1
    while index < n:
        ret = num1
        num1, num2 = num2, num1 + num2
        index += 1
        send_param_data = yield ret  # # yield 关键字的作用挂起函数，并且将函数右面的值返回(调用ret=next(生成器对象)的时候返回给ret)
        # yield 恢复函数的时候可以通过send传参,第一次如果要想用send(None)必须传None 否则can't send non-None value to a just-started generator，yield接收额外的参数赋值给左面可鞥存在的变量
        
        print("接受到了send发送过来的参数值:%s" % send_param_data)
        print("接受到了send发送过来的参数类型:%s" % type(send_param_data))
    
    return  # "我做完了" python2不允许 return 后有值


f = Fib(10)

# for i in f:
#     print i
# print i
# 要想拿到return的返回值,就要自己写一个while循环实现for循环的功能自己捕获异常
tp = 0
while True:
    try:
        if not tp:
            x = next(f)
            tp += 1
        else:
            # pr = Person("裴晓东")  <type 'instance'>
            x = f.send(tp)
            # x = next(f)  # next没有传参相当于send(None)
            tp += 1
            # print("value:%s" % x)
    except StopIteration as e:
        print "生成器返回值%s" % (e)  # e.value也可以
        break
        # time.sleep(5)
    else:
        print("value:%s" % x)
