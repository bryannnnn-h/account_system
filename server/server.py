import socketserver, sys, threading
from time import ctime
import server_config
import sql_connecter

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        db = sql_connecter.db_connecter()
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
        db.closeDB()
            

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    db = sql_connecter.db_connecter()
    server = ThreadedTCPServer((server_config.HOST, server_config.PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    print('server start at: %s:%s' % (server_config.HOST, server_config.PORT))


    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

    


