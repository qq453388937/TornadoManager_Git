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
            (r"/", CookieTest),  # SafeCookie
            (r"/safe", SafeCookie),
            (r"/index", IndexHandler),
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
        self.xsrf_token  # 所有静态文件植入xsrf的cookie 利用浏览器的同源策略
        self.set_secure_cookie("itcast", "oa")
        self.set_secure_cookie("itcast2", "oa2")


class IndexHandler(BaseHandler):
    """渲染模板，加上XSRF校验
    form-data 采用的是自描述，按段落进行描述但是self.get_argument 能接到！
    Content-Disposition: form-data; name="name"
    pxd

    """

    def post(self):
        """

        # pxd_safe="2|1:0|10:1517778127|8:pxd_safe|4:Mg==|c882239d36990732c44df62f6392341550bddb11c9bed20b69fd5eae319e7200"
        #  表单中使用 {% module xsrf_form_html() %}
        :return:
        """

        # 不是表单的话

        # name = self.get_argument("name", "没传过来")
        # pwd = self.get_argument("pwd", "没传过来")
        _xsrf = self.get_argument("_xsrf", "没传过来")
        # print("name:" + name)
        # print("pwd:" + pwd)
        print("_xsrf:" + _xsrf)  # 隐藏域的值
        # print(self.request.body)
        # print(self.request.headers)

        print self.json_dict
        print self.json_dict["name"]
        print self.json_dict["pwd"]
        # print self.request.headers.get("Cookie")  # 打印Cookie的值
        self.write("index post ok！")

    def get(self):
        # 配置过模板路径只需要填写相对路径即可
        self.render("booktest/formpost.html")


class CookieTest(BaseHandler):
    """
    set_cookie(name, value, domain=None, expires=None, path='/', expires_days=None)
    name	cookie名
    value	cookie值
    domain	提交cookie时匹配的域名
    path	提交cookie时匹配的路径
    expires	cookie的有效期，可以是时间戳整数、时间元组或者datetime类型，为UTC时间
    expires_days	cookie的有效期，天数，优先级低于expires
    """

    def get(self):
        # Set-Cookie:pxd="\350\241\214\344\270\232\344\272\272\347\247\260666"; Path=/
        # 手动通过set_header的方式设置cookie
        self.set_header("Set-Cookie", "pxd='\350\241\214\344\270\232\344\272\272\347\247\260666'; Path=/")
        # self.set_cookie("pxd", "行业人称666") # 浏览会话结束时消失
        import time
        import datetime
        # time.strftime()  # 从时间转换为字符串
        # time.strptime()  # 从字符串转换为时间，第一个参数是str的就是字符串转换为时间的取反记忆
        # 利用time.mktime将本地时间转换为UTC标准时间
        if not self.get_cookie("pxd"):
            self.set_cookie("pxd", "123456789",
                            expires=time.mktime(time.strptime("2018-11-11 23:59:59", "%Y-%m-%d %H:%M:%S")))  # 浏览会话结束时消失
            self.write("set cookie ok")
        else:
            value = int(self.get_cookie("pxd"))
            value += 1
            self.set_cookie("pxd", str(value))
            # self.clear_cookie("pxd") #清除name为pxd的cookie
            # self.clear_all_cookies() # 清除所有cookie
            # 经过请求头set-header得知清除cookie仅仅是将过期时间改为以前的时间，并且把内容滞空
            self.write(str(value))

    def post(self):
        self.write(self.request.headers.get("Cookie"))
        self.write("ok")


class SafeCookie(BaseHandler):
    import base64
    import uuid
    uuid.uuid4().bytes  # bytes属性将此uuid码作为16字节字符串。

    uuid.uuid4().get_hex()  # 随机 '06eb32835d894d919c86d9405ed4f5eb' 16进制表示形式
    str(uuid.uuid4())  # '6b0348bb-9d6c-473e-ba88-cf72b6cffaff'  guid
    # 随机混淆
    base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)  # '5wmFAdNoS16eKE3DffS0ZtV9ogd6kUwRhv4/hzj8gzg='
    base64.b64decode('base64解码方法')

    def post(self):
        """
        set_secure_cookie(name, value, expires_days=30)
        设置一个带签名和时间戳的cookie，防止cookie被伪造。
        get_secure_cookie(name, value=None, max_age_days=31)
        如果cookie存在且验证通过，返回cookie的值，否则返回None。max_age_day不同于expires_days，
        expires_days是设置浏览器中cookie的有效期，而max_age_day是过滤安全cookie的时间戳。
        max_age_day 是可以小于 expires_days
        :return:
        """
        cookie_value = self.get_secure_cookie("pxd_safe")
        value = int(cookie_value) + 1 if cookie_value else 1  # python 三元表达式
        self.set_secure_cookie("pxd_safe", str(value))  # cookie:value 字符串必须
        self.write(str(value))  # value 字符串必须


def main():
    tornado.options.parse_command_line()
    app = MyApplication(**config.setting)  # 路由抽取到基类，配置文件单独一个文件
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
