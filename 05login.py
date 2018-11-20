import time
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options

import util.ui_modules
import util.ui_methods
from data.user_modules import User

define('port', default=8000, help='run port', type=int)


class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('01in_out.html')

    def post(self, *args, **kwargs):
        user = self.get_argument('name', '')
        username = User.by_name(user)
        passwd = self.get_argument('password', '')
        if username and passwd == username[0].password:
            self.render('07login.html',
                        username=username,
                        )
        else:
            self.write('用户名或密码错误')




if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/login', LoginHandler),
        ],
        template_path='templates',
        static_path='static',
        ui_methods=util.ui_methods,
        ui_modules=util.ui_modules,
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()