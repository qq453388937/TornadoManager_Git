# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.web import url, RequestHandler, StaticFileHandler
import json
import config
import os

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

    def prepare(self):
        print(os.path.dirname(__file__))
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_dict = json.loads(self.request.body.decode())
        else:
            self.json_dict = None


class IndexHandler(BaseHandler):
    def post(self):
        if self.json_dict:
            for k, v in self.json_dict.items():
                self.write("<h3>%s</h3><p>%s</p>" % (k, v))

    def get(self):

        if self.json_dict:
            for k, v in self.json_dict.items():
                self.write("<h3>%s</h3><p>%s</p>" % (k, v))


class Itcast(BaseHandler):
    def get(self):
        self.write("666")
        #  render 会自动去找 配置好的 template_path 目录下的模板
        # self.render("./index.html")
        # self.render("booktest/index.html")
        context = {
            "price1": "abc",
            "price2": 5555
        }
        #  python 中的语法都可以在前端模板使用！！！！！
        self.render("index.html", **context)
        # self.render("index.html",price1=444,price2=555)


def main():
    tornado.options.parse_command_line()
    current_path = os.path.dirname(__file__)
    app = tornado.web.Application([
        #  这里不能（.*） 否则后面的动态请求就挂了，如果写.* 必须放在最后一个路由判断！!!
        (r"^/api/()$", tornado.web.StaticFileHandler, {
            "path": os.path.join(current_path, "statics/html"),
            "default_filename": "index.html"
        }),
        (r"^/view/(.*)$", tornado.web.StaticFileHandler, {
            # 不设置default_filename 通过用户请求的路径去./static/html/里面去找
            # http://127.0.0.1:9999/static/html/index.html  和statics 文件夹的名字无关，一般设置为static ==》nginx
            "path": os.path.join(current_path, "statics/html")
        }),
        (r"^/itcast$", Itcast)

    ], **config.setting)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
