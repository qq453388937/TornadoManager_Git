# -*- coding:utf-8 -*-
"""
websocekt 的出现是因为http协议是无状态的,被动的
html5 提出的客户端-服务端的通讯协议 协议本身使用ws://URL
1. 前台轮询  间隔请求 ,不断请求
2. 长轮询   请求后有数据改变回应,没有数据改变就不回复任何消息
websocket 用于服务端向浏览器客户端推送消息,前台实时获取消息
h5 规范,客户端和服务端的通讯协议 ws://URL格式  基于tcp,独立创建在tcp上
101 http协议101 状态码进行协议切换  端口也是80
3. websocket
(被动)WebSocketHandler.open() 当一个WebSocket连接建立后被调用。 (被动)
(被动)WebSocketHandler.on_message(message) 当客户端发送消息message过来时被调用，注意此方法必须被重写。
WebSocketHandler.on_close() 当WebSocket连接关闭后被调用。
(主动)WebSocketHandler.write_message(message, binary=False)
向客户端发送消息messagea，message可以是字符串或字典（字典会被转为json字符串）。若binary为False，则message以utf8编码发送；二进制模式（binary=True）时，可发送任何字节码。
(判断源,主动)WebSocketHandler.check_origin(origin)
(主动)WebSocketHandler.close() 关闭WebSocket连接


前端open ==== 后端 onopen
后端write  ==== 前端 onmessage 函数 evt.data
前端send ==== 后端 on_message 函数接收

注意: 后端是不能主动建立websocket链接的
"""
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

define("port", default=1111, type=int)


class WebsocketShowHandler(RequestHandler):
    def get(self):
        self.render("websocket.html")


class WebSocketHandler(WebSocketHandler):  # 继承自WebSocketHandler
    """
    用户链接过来需要容器来保存链接,不能写在__init__里面
    """
    users = []

    def open(self):
        """用户建立链接"""
        self.users.append(self)
        for user in self.users:
            # 上线后向客户端发送消息 向已在线用户发送登陆消息
            user.write_message(
                u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        pass

    def on_message(self, message):
        """客户端发消息过来向所有人推送消息"""
        for user in self.users:  # 向在线用户广播消息
            user.write_message(u"[%s]-[%s]-说：%s" % (
                self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)
                               )

    # def write(self, chunk):
    #     pass

    def on_close(self):
        self.users.remove(self)
        for u in self.users:
            u.write_message(
                u"[%s]-[%s]-离开聊天室,下线了!!!!" % (
                    self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", WebsocketShowHandler),
        (r"/websocket", WebSocketHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), 'statics'),
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
