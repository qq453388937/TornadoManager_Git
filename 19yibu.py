# -*- coding:utf-8 -*-
import time
import threading


#  程序的写法： 回调的方式实现异步！！！！  tornado无非是将线程换成epoll来实现异步

def my_callback(result):
    """回调函数"""
    print result


def new_long_io(param_func=None):
    # 接受一个函数作为参数
    
    def func(callback):
        """执行完线程的方法调用回调函数"""
        print("开始耗时操作～～～～～～～～～～～～～")
        time.sleep(5)
        print("结束耗时操作～～～～～～～～～～～～～～")
        result = "ok！！！！！"
        # return result  # 不再返回
        callback(result)
    
    # th = threading.Thread(target=func)
    # 耗时操作交给别人去处理，这里暂时给一个线程
    th = threading.Thread(target=func, args=(param_func,))
    th.start()
    # th.join()  # join是等线程执行完毕后再继续执行，相当于同步ajax


def old_long_io():
    print "开始耗时操作"
    time.sleep(5)
    print "结束耗时操作"
    ret = "睡完了"
    return ret


def a():
    print("进入请求aaa")
    # 执行一个耗时操作
    # ret = old_long_io()
    # print ret
    
    
    new_long_io(my_callback)  # 新的long_io把打印的任务交给了回调函数去执行
    print ("离开请求aaa！")


def b():
    print("开始请求bbbbbb")
    time.sleep(6)
    print("完成请求bbbbbb")


if __name__ == '__main__':
    a()
    b()
    while True:
        pass
