from copyreg import pickle
import socket, pickle
from client.client_config import IP, PORT
import numpy as np
import pandas as pd
import struct

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
    
    def getTodayMenu(self):
        MenuArray = self.getDatafromServer('Fetch TodayMenu StoreName ItemName price')
        if MenuArray.size != 0:
            todayMenu = pd.DataFrame(MenuArray, columns=['StoreName', 'ItemName', 'price'])
        else:
            todayMenu = pd.DataFrame({'StoreName':['無'], 'ItemName':['無'], 'price':[0]})
        return todayMenu

    def getNameList(self):
        nameList = self.getDatafromServer('Fetch basic_info name')
        return nameList
    
    def getTodayOrderRecordbyName(self, name):
        orderRecordArray = self.getDatafromServer(f'Fetch TodayRecord ItemName amount:StudentName ("{name}")')
        if orderRecordArray.size != 0:
            orderRecord = pd.DataFrame(orderRecordArray, columns=['ItemName', 'amount'])
        else:
            orderRecord = pd.DataFrame()
        return orderRecord
    
    def getDatafromServer(self, msg):
        data_container = np.array([])
        msg = msg.encode()
        self.sock.sendall('GetData'.encode())
        bytes_len = struct.pack('i',len(msg))
        #self.sock.recv(1024)
        self.sock.sendall(bytes_len)
        self.sock.sendall(msg)
        data_len = self.sock.recv(4)
        if data_len != 'none':
            try:
                data_len = struct.unpack('i',data_len)[0]
                recv_len = 0
                recv_data = b''
                while recv_len < data_len:
                    data = self.sock.recv(1024)
                    recv_len += len(data)
                    recv_data += data
                recv_data = pickle.loads(recv_data)
                data_container = recv_data.squeeze()
                self.sock.sendall('s'.encode())
            except Exception as ex:
                self.sock.sendall(str(ex).encode())
        else:
            self.sock.sendall('f'.encode())
        if self.sock.recv(1024).decode() == 'f':
            self.client_error = 'f'

        return data_container
    
    def setTodayOrder(self, orderRecord):
        sql_msg = "set TodayOrder "
        for index, item in orderRecord.iterrows():
            row = f'("StudentName", "ItemName", "price", "amount", "TotalPrice")'
        


    