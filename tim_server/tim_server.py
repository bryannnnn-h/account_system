from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
from time import ctime
import threading

class MyTCPServer(TCPServer):
    def __init__(self, server_address, RequestHandler, bind_and_activate=True, db=None):
        super(MyTCPServer, self).__init__(server_address, RequestHandler, bind_and_activate)
        self.db = db

class ThreadedTCPServer(ThreadingMixIn, MyTCPServer):
    daemon_threads = True
    allow_reuse_address = True

class ThreadedTCPRequestHandler(BaseRequestHandler):
    def handle(self):
        db = self.server.db
        cur = threading.current_thread()
        print('[%s] Client connected from %s and [%s] is handling with him.' % (ctime(), self.request.getpeername(), cur.name))
        while True:
            indata = self.request.recv(1024).strip().decode('utf-8')
            if len(indata) == 0: 
                self.request.close()
                print('client closed connection.')
                break
            print(indata)
            db.dbHandler(indata)
            self.request.sendall('done'.encode())
            


