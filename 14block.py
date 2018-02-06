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
    def get(self):
        self.render("block.html")


class ChildHandler(BaseHandler):
    def get(self):
        self.render("childblock.html")


def main():
    tornado.options.parse_command_line()
    # current_path = os.path.dirname(__file__)
    app = tornado.web.Application([
        #  这里不能（.*） 否则后面的动态请求就挂了，如果写.* 必须放在最后一个路由判断！!!
        # (r"^/api/()$", tornado.web.StaticFileHandler, {
        #     "path": os.path.join(current_path, "statics/html"),
        #     "default_filename": "index.html"
        # }),
        # (r"^/view/(.*)$", tornado.web.StaticFileHandler, {
        #     # 不设置default_filename 通过用户请求的路径去./static/html/里面去找
        #     # http://127.0.0.1:9999/static/html/index.html  和statics 文件夹的名字无关，一般设置为static ==》nginx
        #     "path": os.path.join(current_path, "statics/html")
        # }),
        (r"/", IndexHandler),
        (r"/child", ChildHandler),

    ], **config.setting)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
