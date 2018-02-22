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
    def set_default_headers(self):
        # print("执行了detfault `headers")
        self.set_header("Content-Type", "text/json;charset=UTF-8")
        self.set_header("Itcast", "pxd")

        # 自定义位置参数，自定义多个命名参数放到kwargs的字典里

    def write_error(self, status_code, **kwargs):
        """# send_error(404,content="") 会调用该方法  默认传ｃｏｎｔｅｎｔ是没有意义的
        send_error() 会触发finish() 之后就不能在self.write() 了
        """
        self.set_header("Content-Type", "text/html;charset=UTF-8")
        self.write("出错啦!")
        self.write(u"<h1>出错了，程序员GG正在赶过来！</h1>")
        self.write(u"<p>状态码:%s</p>" % status_code)
        self.write(u"<p>错误详情：%s</p>" % kwargs.get("content", "没传过来哟！"))
        self.write(u"<p>错误名：%s</p>" % kwargs.get("title", "没传过来哟！"))

    def prepare(self):
        if self.request.headers.get("Content-Type").startswith("application/json"):
            self.json_data = json.loads(self.request.body.decode())
        else:
            self.json_data = None


class IndexHandler(BaseHandler):
    # set_status(status_code, reason=None)
    # status_code int类型，状态码，若reason为None，则状态码必须为下表中的。
    # reason string类型，描述状态码的词组，若为None，则会被自动填充为下表中的内容。

    def get(self):
        self.write("index")
        # self.set_header("itcast", "laowang") # 自定义请求头
        # self.set_status(404) # 仅仅是改变了状态码
        # self.set_status(211,"666")
        s = self.get_argument("s")
        a = self.get_argument("a")
        print(type(a))  # python2 拿到的是unicode类型，需要在拼接的时候将拼接字符串转换为u""
        b = self.get_argument("b")
        print(type(b))  # python2 拿到的是unicode类型,需要在拼接的时候讲拼接字符串转化为u“”
        # send_error 会触发write_error 方法,如果重写了的话
        self.send_error(int(s), title="哈哈哈", content="嘿嘿嘿")  # 类似 ｒａｉｓｅ
        # my_dict = {
        #     "title": "行业人称666",
        #     "content": "专业人称999"
        # }
        # #  自动解包
        # self.send_error(200, **my_dict)  # 自动解包
        # self.write("666")

    def write_error(self, status_code, **kwargs):
        self.set_header("Content-Type", "text/html;charset=utf-8")
        self.write("出错啦!")
        self.write(u"<h1>出错了，程序员GG正在赶过来！</h1>")
        self.write(u"<p>状态码:%s</p>" % status_code)
        self.write(u"<p>错误名：%s</p>" % kwargs.get("title", "没传过来哟！"))
        self.write(u"<p>错误详情：%s</p>" % kwargs.get("content", "没传过来哟！"))


class TestHandler(BaseHandler):
    def initialize(self, name):
        self.name = name

    def set_default_headers(self):
        print("执行了detfault `headers")
        self.set_header("Content-Type", "text/html;charset=UTF-8")

    def get(self):
        # self.write(self.name)
        # self.write("666")
        dic = {
            "name": "pxd",
            "age": 18,
            "gender": True
        }
        json_str = json.dumps(dic)  # 对象序列化为json字符串
        # dict_new = json.loads(json_str) # json字符串转换为字典对象
        # self.write(str(dict_new))
        self.write(json_str)
        self.set_header("Content-Type", "application/json;charset=UTF-8")  # 优先级高于set_default_headers



        # self.write(dic) # 直接给字典就会自动转换请求头为application/json  否则默认为text/html


class SendError(BaseHandler):
    def get(self):
        self.write("hello itcast")
        self.send_error(404, content="出现404错误", title="测试title")


class Err404Handler(RequestHandler):
    """对应/err/404"""

    def get(self):
        self.write("hello itcast")
        self.set_status(404)  # 标准状态码，不用设置reason


class Err210Handler(RequestHandler):
    """对应/err/210"""

    def get(self):
        self.write("hello itcast")
        self.set_status(210, "itcast error")  # 非标准状态码，设置了reason


class Err211Handler(RequestHandler):
    """对应/err/211"""

    def get(self):
        self.write("hello itcast")
        self.set_status(211)  # 非标准状态码，未设置reason，错误


def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/test", TestHandler, {"name": "pxd"}),
        (r"/err/211", Err211Handler),
        (r"/err/404", Err404Handler),
        (r"/err/210", Err210Handler),  # SendError
        (r"/SendError", SendError),  #

        # url(r"/cpp", TestHandler, {"name": "666"}, name="cpp"),

    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
