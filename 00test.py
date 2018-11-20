# import tornado.ioloop # 非阻塞套接字的I/O事件循环
# import tornado.web    # web服务器
#
#
# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("hello ")
#
#
# application = tornado.web.Application([
#     (r"/",MainHandler),
# ])
#
# if __name__ == "__main__":
#     application.listen(8080)
#     tornado.ioloop.IOLoop.instance().start()


import tornado.httpserver   # 一个无阻塞的单线程HTTP服务器
import tornado.ioloop
import tornado.options      # 命令行解析模块，让模块定义自己的选项
import tornado.web

from tornado.options import define,options

define('port', default=8000, help='run port', type=int)
define('version', default='0.0.1', help='version 0.0.1', type=str)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('abc')

class AbcIndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('budong')

class TestIndexHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name', 'no')
        self.write('hello '+name)
        print(name)

        name = self.get_arguments('name')
        self.write('<br>')
        self.write(','.join(name))   #write 是不会打印列表表
        print(name)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    print(options.port)
    print(options.version)
    app = tornado.web.Application(
        handlers=[
            (r'/',IndexHandler),
            (r'/abc',AbcIndexHandler),
            (r'/test',TestIndexHandler),
        ],
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()