# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver  # 新导入的httpserver模块
import tornado.options  # 新导入的options模块

"""
关于多进程
虽然tornado给我们提供了一次开启多个进程的方法，但是由于：
每个子进程都会从父进程中复制一份IOLoop实例，如过在创建子进程前我们的代码动了IOLoop实例，那么会影响到每一个子进程，势必会干扰到子进程IOLoop的工作；
所有进程是由一个命令一次开启的，也就无法做到在不停服务的情况下更新代码；
所有进程共享同一个端口，想要分别单独监控每一个进程就很困难。
不建议使用这种多进程的方式，而是手动开启多个进程，并且绑定不同的端口。
"""
# name 唯一  type 可以是str、float、int、datetime、timedelta中的某个
tornado.options.define("port", default=9999, type=int, help="给他一个端口")
tornado.options.define("itcast", default=[1], type=str, help="无意义测试多值情况", multiple=True)


class IndexHandler(tornado.web.RequestHandler):
    """主页处理函数"""

    def get(self):
        """重写父类的方法ＧＥＴ请求的时候会调用该方法"""
        self.write("hello pxd!")


def main():
    # 命令行参数 python 3options.py --port=9999 --itcast=python,java,php,ui
    tornado.options.parse_command_line()
    # tornado.options.options 全局的options对象，所有定义的选项变量都会作为该对象的属性。
    print(tornado.options.options.itcast)
    print(tornado.options.options.port)

    app = tornado.web.Application([(r"/", IndexHandler)])  # 列表嵌套元祖！
    # app.listen(9999)   #  只适用于单进程模式
    # 修改替代上方
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)  # 仅仅是绑定端口不是监听！

    # http_server.bind(9999)
    #  默认开启1个进程,如果设置为 None 或者 0 的话会自动创建和CPU核数相等的进程数,如果>0就是自定义进程数
    #  官方不建议使用自动开启多进程，而是手动开启多个进程绑定不同端口
    # http_server.start(0)
    #              类      实例 有返回无创建 类比单例  这里监听端口
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
