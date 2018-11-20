import time
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options

import util.ui_modules
import util.ui_methods

define('port', default=8000, help='run port', type=int)


class Calculation:
    def sum(self, a, b):
        return a+b


class ExtendlatesHandler(tornado.web.RequestHandler):

    def haha(self):
        return 'this is hahaha'

    def get(self):
        user = self.get_argument('name', 'no')
        urllist = [
            ('https://www.shiguangkey.com/', '时光课堂'),
            ('https://www.baidu.com/', '百度'),
            ('https://www.zhihu.com/', '知乎'),
        ]
        atga = "<a href='https://www.baidu.com' target='_blank'>___百度___</a><br>"  # 转义
        self.render('04extend.html',
                    username=user,
                    time=time,
                    urllist=urllist,
                    atga=atga,
                    haha=self.haha,
                    cal=Calculation
                    )




if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/ext', ExtendlatesHandler),
        ],
        template_path='templates',
        static_path='static',
        ui_methods=util.ui_methods,
        ui_modules=util.ui_modules,
        # ui_modules={'UiModule':util.ui_modules.UiModule, 'Advertisement':util.ui_modules.Advertisement},
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()