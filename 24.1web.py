# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import json
import os

import time

from tornado.options import define, options

define("port", default=1111, help="run on the given port", type=int)



class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "text/html;charset=UTF-8")

    def prepare(self):
        """
               json.loads:JSON str转成dict(python叫字典 javascript叫做对象！！！)
               json.dumps : dict(python叫字典javascript叫做对象！！！！)转成JSON str
        """
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_dict = json.loads(self.request.body.decode())
        else:
            self.json_dict = None


class MyApplication(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        current_path = os.path.join(__file__)
        handlers = [
            (r"/sleep", SleepHandler),
            (r"/justnow", JustNowHandler)
        ]
        super(MyApplication, self).__init__(handlers, **kwargs)


class JustNowHandler(BaseHandler):
    def get(self):
        self.write("i hope just now see you")


#@tornado.web.asynchronous # 只加装饰器是没有用的,前提是执行的函数要执行异步,加上该装饰器后需要手动关闭self.finish()




class SleepHandler(BaseHandler):

    # 第二种方案回调
    @tornado.web.asynchronous
    def get(self):
        tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 10, callback=self.on_response)

    @tornado.web.asynchronous
    def on_response(self):
        self.write("when i sleep 5s")
        self.finish()

    # # 第一种方案
    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    # def get(self):
    #     yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 5)
    #     self.write("when i sleep 5s")





if __name__ == "__main__":
    tornado.options.parse_command_line()
    import config
    app = MyApplication(**config.setting)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
