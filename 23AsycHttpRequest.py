# -*- coding:utf-8 -*-
import time
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.web import url, RequestHandler, StaticFileHandler
import json
import config
import os
import torndb  # 如果有问题安装 pip install mysqlclient 可解决MYSQLDB问题
from tornado.httpclient import AsyncHTTPClient
import tornado.gen

# import tornado.httpclient

tornado.options.define("port", type=int, default=9999, help="端口号")


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # print("执行了detfault `headers")
        self.set_header("Content-Type", "text/html;charset=UTF-8")
    
    def prepare(self):
        """
        json.loads:JSON str转成dict(python叫字典 javascript叫做对象！！！)
        json.dumps : dict(python叫字典javascript叫做对象！！！！)转成JSON str
        """
        print(os.path.dirname(__file__))
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_dict = json.loads(self.request.body.decode())
        else:
            self.json_dict = None


class MyApplication(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        # 路由抽取到基类
        # 这个文件的所在文件夹的绝对路径 == > /home/python/Desktop/TornadoManager/
        current_path = os.path.dirname(__file__)
        
        handlers = [
            (r"/", IndexHandler),  # SafeCookie
            (r"/index", IndexHandler),
            (r"/index2", IndexYieldHandler),
            (r"/index3", BingFaAsyncHandler),
            (r"/other", OtherHandler),
            # OtherHandler  IndexYieldHandler
            # 不用模板语言，直接使用静态文件
            # 这玩意是用来自定义静态资源请求路径的，光靠配置文件的只能/static/html/index.html  ,可以定义多个重复的
            #  如果.*正则匹配和其他路径有可能冲突的话就放在路由映射列表的最后
            # (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(current_path, "statics/html")})
            (r"/(.*)", MyStaticFileHandler, {"path": os.path.join(current_path, "statics/html")}),
            (r"/view/(.*)", MyStaticFileHandler, {"path": os.path.join(current_path, "statics/html")}),
        ]
        # super(子类,self)
        super(MyApplication, self).__init__(handlers, **kwargs)  # 接受过来的参数传给父类
        self.db = torndb.Connection(
            host="127.0.0.1",
            database="test1",
            user="root",
            password="123",  # 看源码得知默认3306端口
        )


class MyStaticFileHandler(tornado.web.StaticFileHandler):
    def __init__(self, *args, **kwargs):
        """只要请求非模板文件，请求静态文件就触发一下xsrf植入cookie
        前段匹配 document.cookie.match("\\b_xsrf=([^;]*)\\b");
        """
        super(MyStaticFileHandler, self).__init__(*args, **kwargs)
        # self.xsrf_token  # 植入cookie 利用浏览器的同源策略
        # self.set_secure_cookie("itcast", "oa")
        # self.set_secure_cookie("itcast2", "oa2")


class IndexHandler(BaseHandler):
    def post(self):
        self.write("index post ok！")
    
    @tornado.web.asynchronous  # 不关闭链接 也不发送响应, 变为异步方法,回调手动过关闭
    def get(self):
        # 配置过模板路径只需要填写相对路径即可
        # 192.168.247.128
        #  实例化异步客户端
        async_client = AsyncHTTPClient()
        remote_url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24"
        async_client.fetch(remote_url, callback=self.callback_func)
    
    def callback_func(self, response):
        """回调函数"""
        body = response.body
        json_data = json.loads(body)
        self.write(json_data["city"])
        self.finish()  # 回调手动关闭 只适用于回调方法方式


class IndexYieldHandler(BaseHandler):
    # @tornado.gen.coroutine
    # def get(self):
    #     async_client = AsyncHTTPClient()
    #     remote_url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24"
    #     response = yield async_client.fetch(remote_url)  # 没有回调
    #     body = response.body
    #     json_data = json.loads(body)
    #     self.write(json_data["city"])
    #     self.finish()
    
    @tornado.gen.coroutine
    def get(self):
        # 一个等一个,排队等 双重等待
        time.sleep(10)
        json_data = yield self.get_ip_city()
        self.write(json_data.get("city"))
        # self.finish() # # 回调手动关闭 只适用于回调方法方式
    
    @tornado.gen.coroutine
    def get_ip_city(self):
        async_client = AsyncHTTPClient()
        remote_url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24"
        
        response = yield async_client.fetch(remote_url)  # 没有回调,同步的写法写异步
        body = response.body
        json_data = json.loads(body)
        # return json_data # python3 可用 python2错误!
        raise tornado.gen.Return(json_data)  # 自定义异常抛出,json_data传进去,唤醒get方法继续执行


class BingFaAsyncHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        """
        并行携程
        Tornado可以同时执行多个异步，并发的异步可以使用列表或字典，如下：
        """
        ips = ["14.130.112.24",
               "15.130.112.24",
               "16.130.112.24",
               "17.130.112.24"]
        # 执行完2个唤醒2个 同时执行多个异步
        rep1, rep2 = yield [self.get_ip_city(ips[0]), self.get_ip_city(ips[1])]  # 返回自己jiebao
        # 再次执行完2个唤醒2个,2个2个异步请求,并行携程
        rep3_and_rep4 = yield {"rep3": self.get_ip_city(ips[2]), "rep4": self.get_ip_city(ips[3])}
        
        self.write_response(ips[0], rep1)
        self.write_response(ips[1], rep2)
        self.write_response(ips[2], rep3_and_rep4['rep3'])
        self.write_response(ips[3], rep3_and_rep4['rep4'])
    
    @tornado.gen.coroutine
    def get_ip_city(self, ip):
        async_client = AsyncHTTPClient()
        remote_url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24"
        response = yield async_client.fetch(remote_url)  # 没有回调
        if response.error:
            json_data = {"ret": "1"}
        else:
            body = response.body
            json_data = json.loads(body)
        # return json_data # python3 可用 python2错误!
        raise tornado.gen.Return(json_data)  # 自定义异常抛出,json_data传进去,唤醒get方法继续执行
    
    def write_response(self, ip, response):
        self.write(ip)
        self.write(":<br/>")
        if 1 == response["ret"]:
            self.write(u"国家：%s 省份: %s 城市: %s<br/>" % (response["country"], response["province"], response["city"]))
        else:
            self.write("查询IP信息错误<br/>")


class OtherHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        time.sleep(1)
        self.write("ok!")
        self.finish()


def main():
    tornado.options.parse_command_line()
    app = MyApplication(**config.setting)  # 路由抽取到基类，配置文件单独一个文件
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
