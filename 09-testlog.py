import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.ioloop import IOLoop
from datetime import timedelta
import time
import os
import sys
import tornado.httpserver
from tornado.options import define, options
import  tornado.options

define('port', default=8000, help='run port', type=int)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    file_content = ""
    filename = "test.log"

    def open(self):
        pass

    def update_client(self):
        self.write_message(self._read_file(self.filename))

    def on_message(self, message):
        print message
        self.filename = message.split('-')[1]
        self.update_client()

    def on_close(self):
        pass

    def _read_file(self, filename):
        print filename, '================='
        with open(filename) as f:
            content = f.read()
            content_diff = content.replace(self.file_content, '')
            self.file_content = content
            return content_diff


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("websockets.html")





if __name__ == '__main__':
    tornado.options.parse_command_line()
    ws_app = tornado.web.Application(
        handlers=[
            (r'/', IndexPageHandler),
            (r'/ws', WebSocketHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()