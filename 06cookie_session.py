import time
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options
from tornado.web import authenticated
from pycket.session import SessionMixin

import util.ui_modules
import util.ui_methods
from data.user_modules import User

define('port', default=8000, help='run port', type=int)



class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):         #必须得重写这方法。
        # current_user = self.get_secure_cookie('ID')
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None



class SetCookieHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_cookie('cookie_test','this_is_test')  #默认过期时间是关闭浏览器
        self.set_cookie('cookie_test1','this_is_test',expires=time.time()+60) #设置的是60秒
        self.set_cookie('cookie_test2','this_is_test',expires_days=1) #设置的是一天
        self.set_cookie('cookie_test3','this_is_test',path='/') #设置路径
        self.set_cookie('cookie_test4','this_is_test',httponly=True) #设置js不可以后去cookie
        self.set_cookie('cookie_test5','this_is_test',max_age=120,expires=time.time()+60) #max_age优先级高
        self.set_secure_cookie('cookie_test6','this_is_test') # 密文，需要设置
        # self.clear_cookie('cookie_test')
        # self.clear_all_cookies()
        self.write('cookie test')


class GetCookieHandler(tornado.web.RequestHandler):

    def get(self):
        get_cookie = self.get_cookie('cookie_test')
        print(get_cookie)
        get_sctatie_cookie = self.get_secure_cookie('cookie_test6')
        print(get_sctatie_cookie)


class LoginHandler(BaseHandler):

    def get(self):
        nextname = self.get_argument('next', '')
        self.render('01in_out.html', nextname=nextname)

    def post(self, *args, **kwargs):
        nextname = self.get_argument('next', '')  #打印的是/buy 不是%2Fbuy  这只是/buy的转码。
        user = self.get_argument('name', '')
        username = User.by_name(user)
        passwd = self.get_argument('password', '')

        if username and passwd == username[0].password:
            # self.set_secure_cookie('ID', username[0].username, max_age=100)
            self.session.set('user', username[0].username)
            # self.render('07login.html',
            #             username=username,
            #             )
            self.redirect(nextname)
        else:
            self.render('01in_out.html', nextname=nextname,error='用户名或密码错误')



class BuyHandler(BaseHandler):

    @authenticated
    def get(self):
        self.write('这个问题冲钱就能解决～～～')





if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/set', SetCookieHandler),
            (r'/get', GetCookieHandler),
            (r'/login', LoginHandler),
            (r'/buy', BuyHandler),
        ],
        template_path='templates',
        static_path='static',
        login_url='/login',   #验证不通过，会跳转到登录页面
        ui_methods=util.ui_methods,
        ui_modules=util.ui_modules,
        cookie_secret='jfshvuh',   #为了把cooker弄成密文。
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