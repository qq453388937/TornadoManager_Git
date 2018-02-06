# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.web import url
import json

tornado.options.define("port", type=int, default=9999, help="端口号")

"""
{
  "form_filename1":[<tornado.httputil.HTTPFile>, <tornado.httputil.HTTPFile>],
  "form_filename2":[<tornado.httputil.HTTPFile>,],
  ...
}
"""


class IndexHandler(tornado.web.RequestHandler):
    def post(self):
        files = self.request.files
        # print(files) # 打印不出来  不建议
        file_model = files.get('my_file')  # name attribute  可以是多个文件一个name

        print(file_model)

        if file_model:  # 有文件,根据表单name键能获取到值
            print(file_model[0].get("filename"))  # 虽然可以点出来但是python 字典只能用[""] | get()
            print(file_model[0].get("content_type"))

            file_data = file_model[0]["body"]
            with open("upload/3.png", "w+") as f:
                f.write(file_data)
            self.write("上传文件ok！")


class SubjectHandler(tornado.web.RequestHandler):
    def initialize(self, name):
        self.name = name

    def get(self):
        self.write(self.name)


def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/python", SubjectHandler, {"name": "pxd"}),
        url(r"/cpp", SubjectHandler, {"name": "666"}, name="cpp"),

    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
