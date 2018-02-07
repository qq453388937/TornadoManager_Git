# -*- coding:utf-8 -*-
import time
import threading
# yield 关键字的作用挂起函数，并且将函数右面的返回

def my_callback(result):
    print result


def new_long_io(param_func):
    def func(callback):
        print "开始耗时操作～～～～～～～"
        time.sleep(5)
        print "结束耗时操作～～～～～～～"
        result = "ok！！！！！"
        # callback(result)
        return result  # 不用回调用yield 返回

    th = threading.Thread(target=func, args=(param_func,))
    th.start()


def a():
    print "进入了a"
    ret = yield new_long_io()
    print ret
    print "离开了a"


def b():
    print "进入了b"

    print "离开了b"


if __name__ == "__main__":
    a()
    b()
    # while True:
    #     pass
