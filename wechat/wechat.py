# -*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import hashlib
import xmltodict
import time
import tornado.gen
import json
import os
import random, string

from tornado.web import RequestHandler
from tornado.options import options, define
from tornado.httpclient import AsyncHTTPClient, HTTPRequest  # 异步客户端

define('port', default=8023, type=int, help='port')
WECHAT_TOKEN = 'itcast'
WECHAT_APP_ID = 'wx6ca414fd5c67b59b'
WECHART_APP_SECRET = '2301ab50f0a9b66859013665fe5e1d5e'
Pin_Duo_Duo = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx6ca414fd5c67b59b&redirect_uri=http%3A//www.idehai.com/wechat8023/profile&response_type=code&scope=snsapi_userinfo&state=110#wechat_redirect"

# http://www.idehai.com/wechat8023/profile?a=b
# ==> 'http%3A//www.idehai.com/wechat8023/profile%3Fa%3Db'
# 无参数正确的: 'http%3A//www.idehai.com/wechat8023/profile'
# import urllib urllib.quote


"""换行两种写法"""


# test1 = "123" \
#         "456"
# test2 = "123\
# 456"


class AccesToken(object):
    _access_token = None  # 默认为空
    _create_time = 0
    _expires_in = 0

    @classmethod
    @tornado.gen.coroutine
    def get_access_token(cls):
        print("cls._createtime ==> %s" % cls._create_time)
        print("cls.__expires_in ==> %s" % cls._expires_in)
        if time.time() - cls._create_time > (cls._expires_in - 200):  # 严格依赖7200秒有问题,给予缓冲
            # 向微信服务器请求access_token
            yield cls.update_access_token()  # 方法内部更新
            raise tornado.gen.Return(cls._access_token)
        else:
            raise tornado.gen.Return(cls._access_token)

    @classmethod
    @tornado.gen.coroutine
    def update_access_token(cls):
        """获取token"""
        client = AsyncHTTPClient()
        remote_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
            WECHAT_APP_ID, WECHART_APP_SECRET)
        resp = yield client.fetch(remote_url)
        json_dict = json.loads(resp.body)
        if 'errcode' in json_dict:
            raise Exception("wechat server error")
        else:
            cls._access_token = json_dict['access_token']
            cls._expires_in = json_dict['expires_in']
            cls._create_time = time.time()


class WechatHandler(RequestHandler):
    """微信接入验证服务器的有效性"""

    def prepare(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        # 微信加密签名,signature结合了开发者填写的tocken参数和请求中的timstamp参数,nonce参数
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument("timestamp", '')  # 时间戳
        nonce = self.get_argument('nonce', '')  # 随机数
        # echostr = self.get_argument('echostr', '')  # 随机字符串 prepare不需要
        # 将token、timestamp、nonce三个参数进行字典序排序
        tmp = [WECHAT_TOKEN, timestamp, nonce]
        tmp.sort()  # sort本身会被修改,sorted([1,2,3,7,4])本身不会修改,返回一个新的
        tm_str = "".join(tmp)
        real_signature = hashlib.sha1(tm_str).hexdigest()  # 字符串的16进制形式
        if real_signature != signature:
            # 请原样返回echostr参数内容
            self.send_error(403)  # forbidden

    def get(self):
        echostr = self.get_argument('echostr', '')
        self.write(echostr)

    def post(self):
        xml_data = self.request.body
        dict = xmltodict.parse(xml_data)
        dict_xml = dict['xml']
        print(dict_xml)
        msg_type = dict_xml['MsgType']
        if msg_type == 'text':
            content = dict_xml['Content']
            """
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[你好]]></Content>
            """
            resp_data = {
                'xml': {
                    'ToUserName': dict_xml['FromUserName'],  # 从哪来回哪去
                    'FromUserName': dict_xml['ToUserName'],  # 从哪来回哪去
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',  # 文本消息
                    'Content': content,
                }
            }
        elif msg_type == 'voice':
            recognition = dict_xml['Recognition']
            print(dict_xml.get('Recognition', u'未能识别出语音'))
            resp_data = {
                'xml': {
                    "ToUserName": dict_xml.get("FromUserName", ""),  # 从哪来回哪去
                    "FromUserName": dict_xml.get("ToUserName", ""),  # 从哪来回哪去
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',  # 文本消息
                    'Content': recognition if recognition else u'未能解析出语音!!',
                    # 'MediaId': dict_xml['MediaId'],
                    # 'Format': dict_xml['Format'],
                    # 'MsgId': dict_xml['MsgId'],
                }
            }
        elif "event" == msg_type:
            if 'subscribe' == dict_xml.get('Event'):
                resp_data = {
                    'xml':
                        {
                            "ToUserName": dict_xml.get("FromUserName", ""),
                            "FromUserName": dict_xml.get("ToUserName", ""),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": u"感谢小包包,小付付的关注！么么哒"
                        }
                }
                if "EventKey" in dict_xml:
                    # 场景值,带二维码的参数
                    event_key = dict_xml['EventKey']
                    scene_id = event_key[8:]
                    resp_data['xml']['Content'] = u"笑而不语%s次" % scene_id

            elif 'SCAN' == dict_xml.get('Event'):
                scene_id = dict_xml['EventKey']
                resp_data = {
                    'xml':
                        {
                            "ToUserName": dict_xml.get("FromUserName", ""),
                            "FromUserName": dict_xml.get("ToUserName", ""),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": u"你扫描的是%s" % scene_id
                        }
                }
            else:
                resp_data = None
        else:
            resp_data = {
                'xml': {
                    'ToUserName': dict_xml['FromUserName'],  # 从哪来回哪去
                    'FromUserName': dict_xml['ToUserName'],  # 从哪来回哪去
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',  # 文本消息
                    'Content': '接受到其他类型的消息非文本',
                }
            }
        print(xmltodict.unparse(resp_data))
        self.write(xmltodict.unparse(resp_data))  # 微信将不做处理,否则会重新发送请求


class QrcodeHandler(RequestHandler):
    """请求微信服务器生成带参数的二维码返回给客户"""

    @tornado.gen.coroutine
    def get(self):
        scene_id = self.get_argument('sid')
        print(scene_id)
        client = AsyncHTTPClient()
        try:
            access_token = yield AccesToken.get_access_token()
        except Exception as e:
            self.write('errmsg:%s' % e)
        else:
            req_data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
            remote_url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % access_token
            request_model = HTTPRequest(
                url=remote_url,
                method="POST",
                body=json.dumps(req_data)
            )
            resp = yield client.fetch(request_model)
            dict_json = json.loads(resp.body)
            if "errcode" in dict_json:
                self.write('errmsg:get qrcode failed')
            else:
                ticket = dict_json['ticket']
                qrcode_url = dict_json['url']
                self.write('<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s"/><br>' % ticket)
                self.write(u"二维码解析之后实际上的url(扫码进入的url):<p>%s</p>" % qrcode_url)


class ProfileHandler(RequestHandler):
    import time
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument('code')  # 接受code
        client = AsyncHTTPClient()
        # 3.通过code换取网页授权access_token
        remote_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (
            WECHAT_APP_ID, WECHART_APP_SECRET, code)
        resp = yield client.fetch(remote_url)
        dict = json.loads(resp.body)
        print(resp.body)
        if "errcode" in dict:
            self.write("error occur !!!!!")
        else:
            # 拿到accesstoken
            access_token = dict['access_token']
            open_id = dict['openid']
            remote_url2 = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" % (
                access_token, open_id)
            resp = yield client.fetch(remote_url2)
            user_data_dict = json.loads(resp.body)
            if "errcode" in user_data_dict:
                self.write("error occur again!!!")
            else:
                self.render('wechat.html', user=user_data_dict, time=JSSDKHandler.get_time())


class MenuHandler(RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        try:
            access_token = yield AccesToken.get_access_token()
        except Exception as e:
            self.write("errmsg: %s" % e)
        else:
            client = AsyncHTTPClient()
            url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
            menu = {
                "button": [
                    {
                        'type': "view",
                        "name": "我的主页",
                        "url": Pin_Duo_Duo,
                    }
                ]
            }
            req = HTTPRequest(
                url=url,
                method="POST",
                body=json.dumps(menu, ensure_ascii=False)
            )
            resp = yield client.fetch(req)
            dict_data = json.loads(resp.body)
            if dict_data['errcode'] == 0:
                self.write('OK')
            else:
                self.write('设置menu失败')


class JSSDKHandler(RequestHandler):
    _access_token = None  # 默认为空
    _create_time = 0
    _expires_in = 0
    _mytime = 0

    @classmethod
    def get_time(cls):
        if cls._mytime - time.time() > 7200:
            cls._mytime = time.time()
        return cls._mytime

    @classmethod
    @tornado.gen.coroutine
    def get_jssdk_access_token(cls):
        """
        https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=ACCESS_TOKEN&type=jsapi
        """
        if time.time() - cls._create_time > (cls._expires_in - 200):  # 严格依赖7200秒有问题,给予缓冲
            # 向微信服务器请求js_access_token
            yield cls.update_jssdk_access_token()  # 方法内部更新
            raise tornado.gen.Return(cls._access_token)
        else:
            raise tornado.gen.Return(cls._access_token)

    @classmethod
    @tornado.gen.coroutine
    def update_jssdk_access_token(cls):
        access_token = yield AccesToken.get_access_token()
        client = AsyncHTTPClient()
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % access_token
        resp = yield client.fetch(url)
        print(resp.body)
        dict_data = json.loads(resp.body)
        if 0 == dict_data.get("errcode"):
            _access_token = dict_data["ticket"]
            print(_access_token)
            cls._access_token = _access_token
            cls._expires_in = dict_data['expires_in']
            cls._create_time = time.time()
        else:
            raise Exception("jssdk server error")

    @classmethod
    @tornado.gen.coroutine
    def get_signature(cls, noncestr, timestamp, url):
        """['jsapi_ticket', 'noncestr', 'timestamp', 'url']"""
        jssdk_token = yield JSSDKHandler.get_jssdk_access_token()
        string = "jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s" % (
            jssdk_token, noncestr, timestamp, url)
        signature = hashlib.sha1(string).hexdigest()
        raise tornado.gen.Return(signature)


class GetTest(RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        jssdk_token = yield JSSDKHandler.get_jssdk_access_token()
        timestamp = JSSDKHandler.get_time()
        signature = yield JSSDKHandler.get_signature('python24', timestamp,
                                                     'http://idehai.com/wechat8023/profile')

        self.write("jssdk_token%s" % jssdk_token)
        self.write('<br>')
        self.write("signture:%s" % signature)


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print (string)
        self.ret['signature'] = hashlib.sha1(string.encode('utf-8')).hexdigest()
        return self.ret


def main():
    tornado.options.parse_command_line()  # 命令行有的转换
    app = tornado.web.Application(
        [
            (r'/wechat8023', WechatHandler),
            (r'/qrcode', QrcodeHandler),  # 自己去使用调用
            (r'/wechat8023/profile', ProfileHandler),
            (r"/menu", MenuHandler),
            (r'/test', GetTest),

        ],
        # 配置模板路径
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'statics'),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
