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
            (r"/sql/(\d*)", SqlHandler),
        ]
        # super(子类,self)
        super(MyApplication, self).__init__(handlers, **kwargs)  # 接受过来的参数传给父类
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

        ret = self.application.db.get("select btitle from bookinfo where id = 7;")
        # ret = MyApplication().db.get("select btitle from bookinfo where id = 2;") 相当于这句话
        print ret  # 字典对象{'btitle': u'\u5929\u9f99\u516b\u90e8'}
        print type(ret)  # <class 'torndb.Row'>
        self.write(ret["btitle"])


class SqlHandler(BaseHandler):
    def get(self, num):
        """ ' or 1=1 or '   sql注入
        db.execute("insert into houses(title, position, price, score, comments) values(%s, %s, %s, %s, %s)", "独立装修小别墅", "紧邻文津街", 280, 5, 128)
或
db.execute("insert into houses(title, position, price, score, comments) values(%(title)s, %(position)s, %(price)s, %(score)s, %(comments)s)", title="独立装修小别墅", position="紧邻文津街", price=280, score=5, comments=128)
        """
        if num == "1":
            sql = "select COUNT(*) as mycount from bookinfo where btitle = %s and bread = %s;"
            # ret = self.application.db.get(sql, "哈哈", 0)
            arg = ("哈哈", 0)
            ret = self.application.db.get(sql, *arg)
            print ret  # 字典对象{'btitle': u'\u5929\u9f99\u516b\u90e8'}
            print type(ret)  # <class 'torndb.Row'>
            print type(ret)  # <class 'torndb.Row'>
            self.write(str(ret["mycount"]))
        elif num == "2":
            sql = "select COUNT(*) as mycount from bookinfo where btitle = %(btitle)s and bread = %(bread)s;"
            # ret = self.application.db.get(sql, "哈哈", 0)
            kwargs = {
                "btitle": "哈哈",
                "bread": 0
            }
            kwargs = dict(  # 这种写法键不用写引号！仅此而已
                btitle="哈哈",
                bread=0
            )
            ret = self.application.db.get(sql, **kwargs)
            # ret = self.application.db.get(sql, btitle="哈哈",bread=0)
            print ret  # 字典对象{'btitle': u'\u5929\u9f99\u516b\u90e8'}
            print type(ret)  # <class 'torndb.Row'>
            self.write(str(ret["mycount"]))
        elif num == "3":
            sql = """insert into pictureinfo(path) VALUES(%s)"""
            # ret = self.application.db.execute(sql, "/pxd/111")  # output inserted id
            ret = self.application.db.execute_rowcount(sql, "/pxd/222")  # output rowcount
            print ret
            self.write(str(ret))

        elif num == "4":
            sql = """select * from bookinfo; """
            try:
                ret = self.application.db.query(sql)
            except Exception as e:
                self.write("DB error:%s" % e)  # 不return就要将下面的放入else
                my_data = {
                    "code": "500",
                    "data": [],
                }
                # self.render("sql.html", **my_data)
                self.write(my_data)
            else:
                my_arr = []
                if ret:
                    for item in ret:
                        my_arr.append({
                            "id": item.id,  # item["id"]
                            "btitle": item["btitle"],  # tornado pz:!S保证了直接用键取不会报错！框架考虑导这个问题不必担心
                            "bcomment": item.get("bcomment"),  # 3种方式都可以他是类字典的对象后俩种推荐
                            "buncuzai": item.get("buncuzai","no !")
                        })
                    my_data = {
                        "code": "200",
                        "data": my_arr,
                    }
                else:
                    my_data = {
                        "data": [],
                        "code": "404",
                    }
                print my_data
                # self.render("sql.html", **my_data)
                self.write(my_data)

    def post(self, num):
        path = self.get_argument("path")
        sql = """insert into pictureinfo(path) VALUES(%s)"""
        try:
            ret = self.application.db.execute(sql, path)
        except Exception as e:
            """return 很关键!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
            return self.write("DB error:%s" % e)  # 不return就要将下面的放入else
        self.write("返回插入的ＩＤ%d" % ret)


def main():
    tornado.options.parse_command_line()
    # current_path = os.path.dirname(__file__)
    # 用自己的Application 原始写法
    # app = MyApplication([
    #     (r"/", IndexHandler),
    # ], **config.setting)

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
