# -*- coding:utf-8 -*-
import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import os

tornado.options.define("port", type=int, default=9999, help="服务器端口设置")
tornado.options.define("itcast", type=str, default=[], help="测试", multiple=True)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello ")


def main():
    tornado.options.parse_command_line()
    # tornado.options.parse_config_file("./config")
    print(tornado.options.options.port)
    print(tornado.options.options.itcast)
    current_path = os.path.dirname(__file__)
    setting = dict(
        static_path=os.path.join(current_path, "static"),
        template_path=os.path.join(current_path, "templates"),
        debug=True,
        autoescape=None
    )
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ], **setting)
    # app.listen()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    # http_server.bind(9999)
    # http_server.start(0)
    # 加一点注释
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
