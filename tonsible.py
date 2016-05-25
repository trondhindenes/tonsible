import tornado.ioloop
import tornado.web
from AnsibleRunner import AnsibleRunner
import time

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        #tornado.ioloop.IOLoop.current().spawn_callback(test)

class GetExecuteAnsiblePlaybookHandler(tornado.web.RequestHandler):
    def get(self):
        tornado.ioloop.IOLoop.current().spawn_callback(exeucte_ansible)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/playbook/", GetExecuteAnsiblePlaybookHandler)
    ])

def exeucte_ansible():
    ansible_runner = AnsibleRunner("package.yml")
    ansible_runner.run()

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()