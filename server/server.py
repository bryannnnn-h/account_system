from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
import os, sys, msvcrt, pickle
import threading
import logging
from sql_connector import db_connecter
import struct

class MyTCPServer(TCPServer):
    def __init__(self, server_address, RequestHandler, bind_and_activate=True):
        super(MyTCPServer, self).__init__(server_address, RequestHandler, bind_and_activate)
        self.serv_logger = self.createServerLogger()
        self.db = db_connecter()
        if self.db.db_error:
            self.serv_logger.error(f"Fail when connecting to db. Please close and restart server after solving problems.\nPress any keys to close...")
            msvcrt.getch()
            self.closeServer(False)
        self.serv_logger.debug(f'server start at {self.server_address}')
    
    def createServerLogger(self):
        serv_logger: logging.Logger = logging.getLogger(name='server')
        serv_logger.setLevel(logging.DEBUG)
        
        s_handler: logging.StreamHandler = logging.StreamHandler()
        f_handler: logging.FileHandler = logging.FileHandler(filename='serverLog.log', mode='w')
        formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        s_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)
        serv_logger.addHandler(s_handler)
        serv_logger.addHandler(f_handler)
        return serv_logger
    
    def closeServer(self,isConnectDB=True):
        if isConnectDB:
            self.db.closeDB()
        self.serv_logger.debug('Server shutdown')
        self.socket.close()
        os._exit(0)


class ThreadedTCPServer(ThreadingMixIn, MyTCPServer):
    daemon_threads = True
    allow_reuse_address = True

class ThreadedTCPRequestHandler(BaseRequestHandler):
    def handle(self):
        db = self.server.db
        serv_logger = self.server.serv_logger
        cur = threading.current_thread()
        try:
            app = self.request.recv(1024).strip().decode()
            self.request.sendall('s'.encode())
            serv_logger.debug(f'connected from {app} and {cur.name} is handling with him.')
        except Exception as ex:
            self.request.sendall(str(ex).encode())
            serv_logger.exception(f'Some errors happen. Please close and restart server after solving problems.\nPress any keys to close...')
            msvcrt.getch()
            self.server.closeServer()
        while True:
            try:                
                indata = self.request.recv(7).strip().decode('utf-8')
                if len(indata) == 0: 
                    self.request.close()
                    serv_logger.debug(f'{app} closed connection.')
                    serv_logger.debug(f'{cur.name} is closed')
                    break
                serv_logger.debug(f'{app} request: {indata}')
                #self.request.sendall('s'.encode())
                if indata == 'GetData':
                    bytes_len = self.request.recv(4)
                    msg_len = struct.unpack('i',bytes_len)[0]
                    indata = self.request.recv(msg_len).strip().decode('utf-8')
                    data = db.dbHandler(indata)
                    if db.db_error:
                        serv_logger.error(f"[{indata}] by [{app}] fail. Please close and restart server after solving problems.\nPress any keys to close...")
                        self.request.sendall('fail'.encode())
                        msvcrt.getch()
                        self.server.closeServer()
                    data = pickle.dumps(data)
                    data_len = len(data)
                    if data_len == 0:
                        serv_logger.debug(f'{indata} gets nothing')
                        self.request.sendall('none'.encode())
                        sendflag = self.request.recv(1024).decode()
                    else:
                        data_len = struct.pack('i',len(data))
                        self.request.sendall(data_len)
                        #sendflag = self.request.recv(1024).decode()
                        #if sendflag != 'f':
                        self.request.sendall(data)
                        sendflag = self.request.recv(1024).decode()
                    if sendflag != 's':                       
                        serv_logger.debug(f'{app} request [{indata}] failed')
                        self.request.sendall('f'.encode())
                    else:
                        serv_logger.debug(f'{app} request [{indata}] done')
                        self.request.sendall('s'.encode())

                elif indata == 'SetData':
                    data_len = self.request.recv(4)
                    data_len = struct.unpack('i',data_len)[0]
                    recv_data = b''

                    #self.request.sendall('s'.encode())
                    try:
                        recv_len = 0
                        while recv_len < data_len:
                            data = self.request.recv(1024)
                            recv_len += len(data)
                            recv_data += data
                        recv_data = recv_data.decode()
                        self.request.sendall('s'.encode())
                    except Exception as ex:
                        self.request.sendall(str(ex).encode())


                    db.dbHandler(recv_data)
                    if db.db_error:
                        serv_logger.error(f"instruction by [{app}] fail. Please close and restart server after solving problems.\nPress any keys to close...")
                        self.request.sendall('fail'.encode())
                        msvcrt.getch()
                        self.server.closeServer()
                    serv_logger.debug(f'{app} request instruction done')
                    self.request.sendall('s'.encode())
            except:
                serv_logger.exception(f'Some errors happen. Please close and restart server after solving problems.\nPress any keys to close...')
                msvcrt.getch()
                self.server.closeServer()

            


