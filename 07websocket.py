import time
import tornado.web
import tornado.ioloop
import tornado.options
import datetime
import tornado.httpserver
from tornado.options import define, options
from tornado.web import authenticated
from pycket.session import SessionMixin
import tornado.websocket

import util.ui_modules
import util.ui_methods
from data.user_modules import User

define('port', default=8000, help='run port', type=int)



class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None

class BaseWebSocketHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None

class Test(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('fsegfdgf')
        print('fsdfdsf')

class LoginHandler(BaseHandler):

    def get(self):
        nextname = self.get_argument('next', '')
        self.render('01in_out.html', nextname=nextname)

    def post(self, *args, **kwargs):
        nextname = self.get_argument('next', '')
        user = self.get_argument('name', '')
        username = User.by_name(user)
        passwd = self.get_argument('password', '')

        if username and passwd == username[0].password:
            self.session.set('user', username[0].username)
            self.redirect(nextname)
        else:
            self.render('01in_out.html', nextname=nextname)



class IndexHandler(BaseHandler):  #普通基类
    @authenticated
    def get(self):
        self.render('08websocket.html')

class MessageWSHandler(BaseWebSocketHandler):
    users = set()     #user是一个集合

    def open(self):
        MessageWSHandler.users.add(self)  # 有新的 WebSocket链接时调用这个函数
        print('-------------------------open------------------')

    def on_message(self, message):
        print(self.request.remote_ip)   #打印的是访问的远程IP地址
        print(self.users)    #打印的是对象
        print(message,self.current_user)   #self.current_user打印的是ywy用户名，因为集成的父类，只有在方法中传入self即可。
        for u in self.users:


            # write_message tornado提供，主动给客户端发送消息
            u.write_message('%s-%s-说：%s'%(
                self.current_user,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                message
                ))


    def on_close(self):
        print('----------------on_close---------------')
        if self in MessageWSHandler.users:
            MessageWSHandler.users.remove(self)
        print(MessageWSHandler.users)


class SyncHanler(BaseHandler):
    def get(self):
        id = self.get_argument('id',1)
        user1 = User.by_id(id)
        time.sleep(10)
        user = {
            'username': user1[0].username,
            'userid': user1[0].id
        }
        self.write(user)



if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/login', LoginHandler),
            (r'/test',Test),
            (r'/', IndexHandler),
            (r'/websocket', MessageWSHandler),
            (r'/sync', SyncHanler),
        ],
        template_path='templates',
        static_path='static',
        login_url='/login',
        ui_methods=util.ui_methods,
        ui_modules=util.ui_modules,
        cookie_secret='jfshvuh',
        pycket={
            'engine': 'redis',
            'storage': {
                'host': '192.168.237.131',
                'port': 6379,
                'db_sessions': 5,
                'db_notifications': 11,
                'max_connections': 2 ** 31,
            },
            'cookies': {
                'expires_days': 30,
                'max_age': 100
            },
        },
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()