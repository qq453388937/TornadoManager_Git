# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.web import url, RequestHandler
import json

tornado.options.define("port", type=int, default=9999, help="端口号")

"""
{
  "form_filename1":[<tornado.httputil.HTTPFile>, <tornado.httputil.HTTPFile>],
  "form_filename2":[<tornado.httputil.HTTPFile>,],
  ...
}
"""


class BaseHandler(tornado.web.RequestHandler):
    """父类Handler可以统一header"""
    def set_default_headers(self):
        # print("执行了detfault `headers")
        self.set_header("Content-Type", "text/html;charset=UTF-8")


        # def write_error(self, status_code, **kwargs):


class IndexHandler(BaseHandler):
    def get(self):
        self.write("主页在这里哟")


class LoginHandler(BaseHandler):
    def get(self):
        self.write('<form method="post"><input type="submit" value="登陆"></form>')

    def post(self):
        self.redirect("/")
        # self.redirect(self.reverse_url('....'))


def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/login", LoginHandler),

    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
