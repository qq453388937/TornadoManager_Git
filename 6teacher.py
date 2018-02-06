# -*- coding:utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.web import url

tornado.options.define("port", type=int, default=9999, help="服务器端口")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):  # reverse_url 是RequestHanlder的方法
        self.write("<a href='%s'>cpp</a>" % (self.reverse_url("cpp_url")))  # 反向解析为r""内


class SubjectHandler(tornado.web.RequestHandler):
    def initialize(self, name):
        self.name = name

    def get(self):
        self.write(self.subject)


def main():
    tornado.options.parse_command_line()  # 命令行的方式,暂时
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/python", SubjectHandler, {"name": "666"}),  # 传入参数到initialize(self,)方法的形参
        url(r"/cpp", SubjectHandler, {"name": "pxd"}, name="cpp_url")  # url方法提供反向解析
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
