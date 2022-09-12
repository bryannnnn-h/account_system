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
    
    def getMenuInfo(self):
        get_msg = f'Fetch MenuRecord ID Year Month Day StoreName:isSelected (True)'
        Menudata = self.getDatafromServer(get_msg)
        date = '0-0-0'
        y, m, d = date.split('-')
        if Menudata.size != 0:
            menuID,y,m,d,storeName = Menudata.squeeze()
            date = '-'.join([str(y),str(m),str(d)])
            MenuArray = self.getDatafromServer(f'Fetch MenuDetail ItemName price:ID ({menuID})')
            todayMenu = pd.DataFrame(MenuArray, columns=['ItemName', 'price'])
        else:
            date = '0-0-0'
            storeName = '無'
            todayMenu = pd.DataFrame()
        return date, storeName, todayMenu

    def getNameList(self):
        nameList = self.getDatafromServer('Fetch basic_info name').squeeze()
        return nameList
    
    def getTodayOrderRecordbyName(self, name):
        orderRecordArray = self.getDatafromServer(f'Fetch TodayRecord ItemName amount:StudentName ("{name}")')
        if orderRecordArray.size != 0:
            orderRecord = pd.DataFrame(orderRecordArray, columns=['ItemName', 'amount']).set_index('ItemName')
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
                data_container = pickle.loads(recv_data)
                self.sock.sendall('s'.encode())
            except Exception as ex:
                self.sock.sendall(str(ex).encode())
        else:
            self.sock.sendall('f'.encode())
        if self.sock.recv(1024).decode() == 'f':
            self.client_error = 'f'

        return data_container
    
    def setTodayRecord(self, order):
        set_msg = "set TodayRecord (Year,Month,Day,StoreName,StudentName,ItemName,price,amount,TotalPrice) "
        for index, item in order.iterrows():
            set_msg += f'(\"{int(item["Year"])}\",\"{int(item["Month"])}\",\"{int(item["Day"])}\",\"{item["StoreName"]}\",\"{item["StudentName"]}\",\"{item["ItemName"]}\",{int(item["price"])},{int(item["amount"])},{int(item["TotalPrice"])}),'
        self.setDataByServer(set_msg)
    
    def deleteTodayRecord(self, name):
        delete_msg = f'Delete TodayRecord:StudentName ("{name}")'
        self.setDataByServer(delete_msg) 

    def setDataByServer(self, setDataMsg):
        self.sock.sendall('SetData'.encode())
        setDataMsg = setDataMsg.encode()
        byte_len = struct.pack("i", len(setDataMsg))            
        self.sock.sendall(byte_len)
        self.sock.sendall(setDataMsg)
        if self.sock.recv(1024).decode() == 'f':
            self.client_error = 'f'
        if self.sock.recv(1024).decode() == 'f':
            self.client_error = 'f'
        


    