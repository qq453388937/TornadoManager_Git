# coding:utf-8
import tornado.web
import tornado.ioloop


class IndexHandler(tornado.web.RequestHandler):
    """主页处理函数"""

    def get(self):
        """重写父类的方法ＧＥＴ请求的时候会调用该方法"""
        self.write("hello world")  # 再次封装http报文，响应码之类


def main():
    app = tornado.web.Application([(r"/", IndexHandler)])  # 列表嵌套元祖！
    app.listen(9999)  # 仅仅是绑定端口不是监听！
    #              类      实例 有返回无创建 类比单例
    tornado.ioloop.IOLoop.current().start()  # 这里监听端口！


if __name__ == "__main__":
    main()
