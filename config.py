# -*- coding:utf-8 -*-
import os

redis_options = {
    'redis_host': '127.0.0.1',
    'redis_port': 6379,
    'redis_pass': '',

}
"""
另一个好处是你可以改变你应用URL的结构，而不需要改变模板中的代码。
例如，可以通过设置static_url_prefix来更改Tornado的默认静态路径前缀/static。
如果使用static_url而不是硬编码的话，代码不需要改变。

"""
# 这些个键是固定的参数
setting = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),  # 设置模板路径，如果用到模板和django一样的话
    # tornado static_path = os.path.join(os.path.dirname(__file__),"statics")  这个参数是配置静态文件的目录的
    # 但请求静态资源路径是/static/开头这个是固定的而不是文件夹的名字statics开头注意！！！！
    # http://127.0.0.1:9999/static/html/index.html  和statics 文件夹的名字无关，一般设置为static ==》nginx
    # /static/html/index.html
    'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
    'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
    # 'static_url_prefix': "/ChinaNumber1", # 一般默认用/static ,这个参数可以修改默认的静态请求开头路径
    'cookie_secret': '0Q1AKOKTQHqaa+N80XhYW7KCGskOUE2snCW06UIxXgI=',  # 组合拳
    #'xsrf_cookies': True,  # 组合拳
    # 校验不通过也就是一般来说的登陆失败后跳转的页面地址
    'login_url': '/login',  # 登陆验证 用户验证  @tornado.web.authenticated 重写 Requesthandler.get_current_user(self): return true则通过校验！
    # 'autoescape':True
    # 'autoreload':True
    'debug': True,
}

# 日志
log_path = os.path.join(os.path.dirname(__file__), 'log')
