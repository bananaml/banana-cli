
prepare_env = '''
import threading, os
from werkzeug.serving import make_server

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 8000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
'''

run_init = "app.init_func()"

start_server = '''
flask_app = app._create_flask_app()
server = ServerThread(flask_app)
server.start()
'''

stop_server = "server.stop()"

stop_server_quietly = '''
try:
    server.stop()
except:
    pass
'''