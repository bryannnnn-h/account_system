from copyreg import pickle
import socket, pickle
from client.client_config import IP, PORT
import numpy as np

class client_orderSystem():
    def __init__(self):
        self.sock, self.client_error = self.connectServer()
    
    def connectServer(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        sock.sendall('OrderSystem'.encode())
        receive_signal = sock.recv(1024).strip().decode()
        client_error = None
        if receive_signal != 's':
            client_error = receive_signal
        return sock, client_error

    def getNameList(self):
        nameList = np.array([])
        self.sock.sendall('GetData Fetch basic_info name'.encode())
        data_len = self.sock.recv(1024).strip().decode()
        if data_len != 'empty':
            self.sock.sendall('s'.encode())
            try:
                data_len = int(data_len)
                recv_len = 0
                recv_data = b''
                while recv_len < data_len:
                    data = self.sock.recv(1024)
                    recv_len += len(data)
                    recv_data += data
                recv_data = pickle.loads(recv_data)
                nameList = recv_data.squeeze()
                self.sock.sendall('s'.encode())
            except Exception as ex:
                self.sock.sendall(str(ex).encode())
        else:
            self.sock.sendall('f'.encode())
        if self.sock.recv(1024).decode() == 'f':
            self.client_error = 'f'
        return nameList
    
    def saveTodayOrder(self, orderRecord):
        pass
        


    