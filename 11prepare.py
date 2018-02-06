# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.web import url, RequestHandler, StaticFileHandler  # 静态文件用到的！
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
    def set_default_headers(self):
        # print("执行了detfault `headers")
        self.set_header("Content-Type", "text/html;charset=UTF-8")


        # def write_error(self, status_code, **kwargs):


class IndexHandler(BaseHandler):
    def prepare(self):
        """
        因为get 和 post 只能收到Content-Type 为 form-data | x-www-form-urlencoded 两种类型的请求
        所以想要对发过来为json数据进行一个预处理存起来就可以使用啦！
        # None.startswith会报错，不安全，所以要给Content-Type给一个空字符串的默认值
        :return:
        """
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_dict = json.loads(self.request.body.decode("utf-8"))
        else:
            self.json_dict = None

    def on_finish(self):
        print("on_finish")

    def post(self):
        if self.json_dict:
            for k, v in self.json_dict.items():
                self.write("<h3>%s</h3><p>%s</p>" % (k, v))

    def get(self):
        if self.json_dict:
            for k, v in self.json_dict.items():
                self.write("<h3>%s</h3><p>%s</p>" % (k, v))


class Index2Handler(RequestHandler):
    def initialize(self):
        print("调用了initialize()")

    def prepare(self):
        print("调用了prepare()")

    def set_default_headers(self):
        print("调用了set_default_headers()")

    def write_error(self, status_code, **kwargs):
        print("调用了write_error()")

    def get(self):
        print("调用了get()")

    def post(self):
        print("调用了post()")
        self.send_error(200)  # 注意此出抛出了错误

    def on_finish(self):
        print("调用了on_finish()")


def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/index2", Index2Handler),

    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
