# -*- coding:utf-8 -*-
# mysql -u root -p[123] < db.sql,
# createTime datetime default current_timestamp ,
# updateTime datetime default curremt_timestamp
# on update current_timestap ,
# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.web import url, RequestHandler, StaticFileHandler
import json
import config
import os
import torndb  # 如果有问题安装 pip install mysqlclient 可解决MYSQLDB问题

tornado.options.define("port", type=int, default=9999, help="端口号")


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # print("执行了detfault `headers")
        self.set_header("Content-Type", "text/html;charset=UTF-8")

    def prepare(self):
        print(os.path.dirname(__file__))
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_dict = json.loads(self.request.body.decode())
        else:
            self.json_dict = None

    # 这里可以校验用户登陆的方法
    def get_current_user(self):
        """这里校验session有值正确则返回True,否则返回False,这里假设name参数为session的值模拟登陆流程 请求127.0.0.1:8000/"""
        # return "366"
        # 假设能接收导a的值就认为是登陆成功  仅仅是演示重定向登陆成功
        # f = self.get_argument("name", None)
        # if f:
        #     return True
        # else:
        #     return False
        return False





class MyApplication(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        # 路由抽取到基类
        current_path = os.path.dirname(__file__)
        handlers = [
            (r"/", IndexHandler),  # SafeCookie
            (r"/index", IndexHandler),
            (r"/login", LoginHandler),
            # 不通过模板去提供静态资源，er是静态资源
            # (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(current_path, "statics/html")})
            (r"/(.*)", MyStaticFileHandler, {"path": os.path.join(current_path, "statics/html")})
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
        """只要请求静态文件就触发一下xsrf植入cookie
        前段匹配 document.cookie.match("\\b_xsrf=([^;]*)\\b");
        """
        super(MyStaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token  # 植入cookie
        self.set_secure_cookie("itcast", "oa")
        self.set_secure_cookie("itcast2", "oa2")


class IndexHandler(BaseHandler):
    def post(self):
        self.write("ok111")

    @tornado.web.authenticated
    def get(self):
        self.render("formpost.html")


class LoginHandler(BaseHandler):
    def get(self):
        """这里一系列登陆处理等操作"""
        next_url = self.get_argument("next", "")
        return self.write("登陆页面，伪代码")
        # print(next_url)
        # if next_url:
        #     self.redirect(next_url + "?name=logined")
        # else:
        #     self.write("登陆页面，伪代码")


def main():
    tornado.options.parse_command_line()
    app = MyApplication(**config.setting)  # 路由抽取到基类，配置文件单独一个文件
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
