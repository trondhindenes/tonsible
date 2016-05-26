import tornado.ioloop
import tornado.web
from flask.config import Config
from tornado import gen
from AnsibleRunner import AnsibleRunner
import time
from OptionParser import OptionParser
import tornado.autoreload

class MyConfig:
    counter = 0

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        #tornado.ioloop.IOLoop.current().spawn_callback(test)

class GetExecuteAnsiblePlaybookHandler(tornado.web.RequestHandler):
    def post(self, playbookname=None):
        data = tornado.escape.json_decode(self.request.body)
        MyConfig.counter = MyConfig.counter + 1


        playbook, options = OptionParser.parse_opts(data, playbookname)
        tornado.ioloop.IOLoop.current().spawn_callback(exeucte_ansible, playbook, options)
        self.write(str(MyConfig.counter))

def make_app():
    return tornado.web.Application([
            (r"/", MainHandler),
            (r"/playbook", GetExecuteAnsiblePlaybookHandler),
            (r"/playbook/(?P<playbookname>[^\/]+)", GetExecuteAnsiblePlaybookHandler)]
    )



@gen.coroutine
def exeucte_ansible(playbook, options):
    ansible_runner = AnsibleRunner(playbook, options)
    ansible_runner.run()

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.current().start()