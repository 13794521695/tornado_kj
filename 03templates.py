import time
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options

define('port', default=8000, help='run port', type=int)


class TemplatesHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('templates')   #依然会在跳转页面上的头部打印template。
        # self.render('01in_out.html')
        self.render('test.html')

    def post(self, *args, **kwargs):
        user = self.get_argument('name', 'no')
        urllist = [
            ('https://www.shiguangkey.com/', '时光课堂'),
            ('https://www.baidu.com/', '百度'),
            ('https://www.zhihu.com/', '知乎'),
        ]
        atga = "<a href='https://www.baidu.com' target='_blank'>___百度___</a><br>"  # 转义
        self.render('02templates.html',
                    username=user,      #可以用到这里面的变量
                    time=time,          #时间模块time传入到模拟里，模板也能直接调用函数。
                    urllist=urllist,
                    atga=atga,
                    )




if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/tem', TemplatesHandler),
        ],
        template_path='templates',
        static_path='static',
        autoescape=None,     #可以让所有模板文件取消转义。
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()