# -*- coding:utf-8 -*-
import time
import threading

# yield 关键字的作用挂起函数，并且将函数右面的返回

gen_model = None


def new_long_io():
    # 接受一个函数作为参数
    
    def func():
        """执行完线程的方法调用回调函数"""
        global gen_model
        print("开始耗时操作～～～～～～～～～～～～～")
        time.sleep(5)
        print("结束耗时操作～～～～～～～～～～～～～～")
        result = "ok！！！！！"
        # return result  # 开始不再返回,现在return回去
        try:
            gen_model.send(result)
        except StopIteration as e:
            pass
            
            # th = threading.Thread(target=func)
    
    # 耗时操作交给别人去处理，这里暂时给一个线程
    th = threading.Thread(target=func)
    th.start()
    
    # th.join()  # join是等线程执行完毕后再继续执行，相当于同步ajax


def a():
    print "进入了a"
    # 使用yield 就不用回调了
    ret = yield new_long_io()
    print ret
    print "离开了a"


def b():
    print "进入了b"
    time.sleep(3)
    print "离开了b"


if __name__ == "__main__":
    # 方法里用全局变量需要用global申明,如果是if语句则不需要global申明使用全局变量
    gen_model = a()  # a函数有yield所以是生成器,不能直接调用
    next(gen_model)
    b()
    while True:
        pass
