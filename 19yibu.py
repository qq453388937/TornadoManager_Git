# -*- coding:utf-8 -*-

def long_io():
    import time
    print("开始耗时操作")
    time.sleep(5)
    print("结束耗时操作")
    return "ok"

def a():
    print("进入请求aaa")
    long_io()
    print ("完成请求aaa")


def b():
    print("开始请求bbbbbb")
    print("完成请求bbbbbb")


if __name__ == '__main__':
    a()
    b()
