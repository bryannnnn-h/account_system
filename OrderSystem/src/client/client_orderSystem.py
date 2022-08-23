import socket
from client_config import IP, PORT

class client_orderSystem():
    def __init__(self):
        self.sock, self.client_error = self.connectServer()

        self.nameList = self.getNameList()
    
    def connectServer(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        sock.sendall('OrderSystem'.encode())
        receive_signal = sock.recv(1024).strip().decode()
        if receive_signal != 's':
            client_error = receive_signal
        return sock, client_error

    def getNameList(self):
        self.sock.sendall('Fetch basic_info name')


    