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
        # def write_error(self, status_code, **kwargs):

    def prepare(self):
        print(os.path.dirname(__file__))
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_dict = json.loads(self.request.body.decode())
        else:
            self.json_dict = None


class MyApplication(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        # 路由抽取到基类
        handlers = [
            (r"/", IndexHandler),
        ]
        # super(子类,self)
        super(MyApplication, self).__init__(handlers, **kwargs)  # 接受过来的参数传给父类,但是hanlers路由映射是子类穿过去的
        self.db = torndb.Connection(
            host="127.0.0.1",
            database="test1",
            user="root",
            password="123",  # 看源码得知默认3306端口
        )


class IndexHandler(BaseHandler):
    def get(self):
        """
execute(query, *parameters, **kwparameters) 返回影响的最后一条自增字段值
execute_rowcount(query, *parameters, **kwparameters) 返回影响的行数
         """
        # 因为基类中RequestHandler的__init__方法封装了属性application为Application的实例对象
        ret = self.application.db.get("select btitle from bookinfo where id = 7;")
        # ret = MyApplication().db.get("select btitle from bookinfo where id = 2;") 相当于这句话
        print ret  # 字典对象{'btitle': u'\u5929\u9f99\u516b\u90e8'}
        print type(ret)  # <class 'torndb.Row'>
        self.write(ret["btitle"])


def main():
    tornado.options.parse_command_line()
    # current_path = os.path.dirname(__file__)
    # 用自己的Application 原始写法
    # app = MyApplication([
    #     (r"/", IndexHandler),
    # ], **config.setting)
    # 路由映射抽取导MyApplication中
    app = MyApplication(**config.setting)  # 路由抽取到基类，配置文件单独一个文件
    # 最简版本抽取到基类自己的Application
    # app.db = torndb.Connection(
    #     host="127.0.0.1",
    #     database="test1",
    #     user="root",
    #     password="123",  # 看源码得知默认3306端口
    # )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
