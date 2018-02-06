# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.web import url
import json

tornado.options.define("port", type=int, default=9999, help="端口号")


class IndexHandler(tornado.web.RequestHandler):
    def post(self):
        """
        只能获取Content-Type 为application/x-www-form-urlencoded
        和 Content-Type 为multipart/form-data 2种类型的用下列方法接受
        参数,对于json和xml的无法通过下列方法获取
        :return:
        """
        # param_get = self.get_query_argument("a", "没有传过来哟")  # 不设置默认值必须传参数a，传多个收一个会只收最后一个
        # params_get = self.get_query_arguments("a", "没有传过来哟")
        # param_post = self.get_body_argument("b", "没有传过来哟")
        # params_post = self.get_body_arguments("b", "没有传过来哟")
        # param_all = self.get_argument("a", "没有传过来哟")
        # param_all_info = self.get_arguments("a", "没有传过来哟")
        # self.write(str(param_get))  # 只认识字符串，不能像print一样直接输出数组
        # self.write(str(params_get))  # 只认识字符串，不能像print一样直接输出数组
        # self.write(str(param_post))  # 只认识字符串，不能像print一样直接输出数组
        # self.write(str(params_post))  # 只认识字符串，不能像print一样直接输出数组
        # self.write(param_all)
        # self.write(str(param_all_info))
        # self.write("<a href='%s'>cpp</a>" % (self.reverse_url("cpp")))

        """self.request 对象"""
        print(self.request.headers)  # request.headers 是类似字典的对象可以用get
        print(self.request.headers.get("Content-Type"))  # self.body 是２进制需要ｄｅｃｏｄｅ
        print(self.request.body.decode())
        if self.request.headers.get("Content-Type").startswith("application/json"):
            json_str2 = self.request.body.decode()  # 刚转过来是str字符串，ｊｓｏｎ字符串
            # print(type(json_str2)) # str
            json_str = eval(self.request.body.decode())  # 字符串转字典，转成他应该的类型
            # json_model = json.load(json_str2) # no xing teacher can
            self.write(json_str)
            # print(type(json_str))
            # print(json_str["name"])
            self.write(json_str["name"])  # Raw才能看到 pretty显示方式会忽略


class SubjectHandler(tornado.web.RequestHandler):
    def initialize(self, name):
        self.name = name

    def get(self):
        self.write(self.name)


class RegexHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self, num1, num2):
        self.write("正则表达式第一个位置参数为%s<br>" % (str(num1)))
        self.write("正则表达式第二个位置参数为%s<br>" % (str(num2)))


class Regex2Handler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self, age, name):
        self.write("正则表达式第一个位置参数为%s<br>" % (str(name)))
        self.write("正则表达式第二个位置参数为%s<br>" % (str(age)))


def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        # 还有autoreload=true ,compiled_template_cache=False  static_hash_cache=False  serve_traceback=True 详细看课件Application
        (r"/", IndexHandler),
        (r"/python", SubjectHandler, {"name": "pxd"}),
        # 位置参数
        url(r"/regex/(\d+)/(.*)", RegexHandler, {}, name="regex"),
        # 命名参数
        url(r"/regex2/(?P<name>\d+)/(?P<age>.*)", Regex2Handler, {}, name="regex2"),
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
