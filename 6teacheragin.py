# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.web import url

tornado.options.define("port", type=int, default=9999, help="端口号")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<a href='%s'>cpp</a>" % (self.reverse_url("cpp")))


class SubjectHandler(tornado.web.RequestHandler):
    def initialize(self, name):
        self.name = name

    def get(self):
        self.write(self.name)


def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/python", SubjectHandler, {"name": "pxd"}),
        url(r"/cpp", SubjectHandler, {"name": "666"}, name="cpp"),

    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
