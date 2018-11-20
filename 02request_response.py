import time
import tornado.web
import tornado.ioloop
import tornado.options      # 命令行解析模块，让模块定义自己的选项
import tornado.httpserver   # 一个无阻塞的单线程HTTP服务器
from tornado.options import define, options

define('port', default=8000, help='run port', type=int)


class HeaderHandler(tornado.web.RequestHandler):
    def get(self):                          #设置响应头
        self.write('set_header')
        self.set_header('aaa', '1111')
        self.set_header('bbb', '2222')
        self.set_header('bbb', '3333')


class AddHandler(tornado.web.RequestHandler):
    def get(self):                           #添加响应头，可以设置一样的
        self.write('add_header')
        self.add_header('ccc', '3333')
        self.add_header('ccc', '4444')


class CleanHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('clear_heander')
        self.add_header('abcd', '5555')
        self.add_header('abcd', '6666')
        self.clear_header('abcd')   #可以撤销写的响应头


class SendHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('send_error')
        # self.flush()      不能加flush()， 不然不会执行下面的404
        self.send_error(404)   #上面的写入是在缓存，但是遇到下面的send_error会丢弃之前的缓存，直接跳转404
           #send_error底层调用的就是write_error这个方法。
    def write_error(self, status_code, **kwargs):
        self.write('status_code: %s' % status_code)


class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('set_status')  #正常打印，后面的404状态码会在控制台返回
        # self.set_status(404)
        self.set_status(404, 'error')


class IndexHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print(' ---set_default_headers---:设置header')

    def initialize(self):
        print(' ---initialize---:初始化')

    def prepare(self):
        print(' ---prepare---：准备工作')

    def get(self):
        self.write(' ---get---：处理get请求'+'<br>')

    def post(self):
        self.write(' ---post---：处理post请求'+'<br>')

    def write_error(self, status_code, **kwargs):
        print(' ---write_error---：处理错误')

    def on_finish(self):
        print(' ---on_finish---：结束，释放资源')

class NotFoundHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.send_error(404)      #底层调用write_error，直接返回错误页面。

    def write_error(self, status_code, **kwargs):
        self.render('error_notfound.html')


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/header', HeaderHandler),
            (r'/add', AddHandler),
            (r'/clear', CleanHandler),
            (r'/send', SendHandler),
            (r'/status', StatusHandler),
            (r'/index', IndexHandler),
            (r'/(.*)', NotFoundHandler),
        ],
        template_path='templates',
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
