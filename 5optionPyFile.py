# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver  # 新导入的httpserver模块
import tornado.options  # 新导入的options模块
import config  # 新导入的自定义的py文件

# name 唯一  type 可以是str、float、int、datetime、timedelta中的某个
tornado.options.define("port", default=8001, type=int, help="给他一个端口")
tornado.options.define("itcast", default=[1], type=str, help="无意义测试多值情况", multiple=True)

class IndexHandler(tornado.web.RequestHandler):
    """主页处理函数"""

    def get(self):
        """重写父类的方法ＧＥＴ请求的时候会调用该方法"""
        self.write("hello pxd!")


def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler)
    ], **config.setting)  # 列表嵌套元祖！
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)  # 仅仅是绑定端口不是监听！
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
