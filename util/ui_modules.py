'''
this is ui_modules
'''
from tornado.web import UIModule

class UiModule(UIModule):
    def render(self, *args, **kwargs):   #此方法必须重写
        return '我是 ui_module'

class  Test(UiModule):
    def render(self, *args, **kwargs):      #当模板调用这个类时， render会自动执行
        return '你好'
    def haha(self):
        return '100'
    def hehe(self):
        return '200'

class Advertisement(UIModule):
    def render(self, *args, **kwargs):
        return self.render_string('06ad.html')

    def css_files(self):
        return "/static/css/King_Chance_Layer7.css"
    def javascript_files(self):
        return [
            "/static/js/jquery_1_7.js",
            "/static/js/King_Chance_Layer.js",
            "/static/js/King_layer_test.js",
        ]