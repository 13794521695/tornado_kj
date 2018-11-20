import time
import tornado.web
import tornado.ioloop
import tornado.options      # 命令行解析模块，让模块定义自己的选项
import tornado.httpserver   # 一个无阻塞的单线程HTTP服务器
from tornado.options import define, options

define('port', default=8000, help='run port', type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(b'Tornado <br>')
        self.write('<b>Tornado</b><br>')
        # self.flush()
        # time.sleep(3)
        # self.write('<b>Tornado</b><br>')   #先写到缓冲区，然后再统一写到界面上
        # self.flush()
        # self.write('<b>Tornado</b><br>')
        # user = {
        #     'name': 'budong',
        #     'age': 18
        # }
        # self.write(user)        #字典可以直接打印
        # li = [1, 2, 3, 4]
        # import json
        # li = json.dumps(li)        #把列表dumps成字符串。
        # self.write(li)        #write 参数里面只能是byte,字典 或者unicode
        # print(repr(li))
        # li = json.loads(li)
        # print(repr(li))
        # self.flush()
        # self.write('OK!!!')
        # self.finish()             #self.finsh()后不能再接write，不然会报错。
        self.write('finish')
        print(self.request.headers)
        print(self.request.body)


class TemHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('this is Tornado <br>')  #先打印然后再跳转页面，这个会执行
        self.render('test.html')  #经过测试，这是能正确跳转的。
        # self.render('01in_out.html')


class RecHandler(tornado.web.RequestHandler):
    def get(self):
        import time
        time.sleep(3)
        self.redirect(r'/tem')


class ReqHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(self.request.remote_ip)  #输出请求IP
        print(self.request.remote_ip)
        print(self.request.connection)      #输出连接状态
        print(self.request.full_url())      #输出完整的URL包括端口以及路由
        print(self.request.request_time())  #请求的时间戳
        print(self.request.uri)             #输出/req
        print(self.request.path)            #输出/req
        print(dir(self.request))
        print(self.request)                     #输出请求的详细信息


class GetHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name', 'no')
        self.write(name)
        self.write('<br>')                       #get的方法是获取url传参
        name = self.get_arguments('name')
        self.write('<br>'.join(name))
        qu = self.get_query_argument('name', 'query')
        print(qu)
        print(self.request.body)

    def post(self, *args, **kwargs):            #post方法是前端html页面的action提交的路由过来的，这里就可以获取。
        name = self.get_argument('name', 'no')
        passwd = self.get_argument('password', 'none')
        self.write('user: %s <br> password: %s' % (name, passwd))
        bo = self.get_body_argument('name', 'body')
        print(bo)


class UserHandler(tornado.web.RequestHandler):   #URL传参
    def get(self, name, age):
        self.write('name: %s <br> age: %s' % (name, age))


class StudentHandler(tornado.web.RequestHandler):
    def get(self, name, number):
        self.write('name: %s <br> number: %s' % (name, number))


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/tem', TemHandler),
            (r'/rec', RecHandler),
            (r'/req', ReqHandler),
            (r'/get', GetHandler),
            (r'/user/(.+)/([0-9]+)', UserHandler),
            (r'/stu/(?P<number>[0-9]+)/(?P<name>.+)', StudentHandler),
        ],
        template_path='tornado_fk1/templates',
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

# http://127.0.0.1:8000/user/budong/18
# http://127.0.0.1:8000/stu/20170001/budong
