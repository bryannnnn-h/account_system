import socket
from client.client_config import *
import sys
import pandas as pd
import numpy as np
import struct
import pickle

class clientHandler:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IP, PORT))
        self.sock.sendall('accountSystem'.encode())
        self.sock.recv(1024)

    def setMenuDetail(self, y, m, d, df):
        self.setDataByServer(f'Delete MenuDetail:Year ({y})&Month ({m})&Day ({d})')
        todayMsg = 'set MenuDetail (Year,Month,Day,StoreName,ItemName,price) '
        for index, item in df.iterrows():
            todayMsg += f'({y},{m},{d},\"{item["StoreName"]}\",\"{item["ItemName"]}\",{int(item["price"])}),'

        self.setDataByServer(todayMsg)
    
    def setMenuRecord(self, y, m, d, storeName):
        self.setDataByServer(f'Delete MenuRecord:Year ({y})&Month ({m})&Day ({d})')
        set_msg = f'set MenuRecord (Year,Month,Day,StoreName,isSelected,isCompleted) ({y},{m},{d},"{storeName}",False,False)'
        self.setDataByServer(set_msg)

    def addFavMenu(self, df):   
        FavMsg = 'set FavMenu (StoreName,FavMenuName,ItemName,price) '
        for index, item in df.iterrows():
            FavMsg += f'(\"{item["StoreName"]}\","{item["FavMenuName"]}\",\"{item["ItemName"]}\",{int(item["price"])}),'
        self.setDataByServer(FavMsg)

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


    def getFavNameList(self):
        FavNameList = self.getDatafromServer('Fetch FavMenu FavMenuName').squeeze()
        FavNameList = np.unique(FavNameList)
        return FavNameList

    def getFavMenuContent(self,FavName):
        FavMenuArray = self.getDatafromServer(f'Fetch FavMenu StoreName ItemName price:FavMenuName ("{FavName}")')
        if FavMenuArray.size != 0:
            FavMenuContent = pd.DataFrame(FavMenuArray, columns=['StoreName', 'ItemName', 'price'])
        else:
            FavMenuContent = pd.DataFrame()
        return FavMenuContent

    def getTableContent(self,TableName):
        TableArray = self.getDatafromServer(f'Fetch {TableName} *')
        columnArray = self.getDatafromServer(f'showColumn {TableName}')
        if TableArray.size != 0:
            TableContent = pd.DataFrame(TableArray, columns=columnArray)
        else:
            TableContent = pd.DataFrame()
        return TableContent

    def getTodayRecord(self):
        TodayRecordArray = self.getDatafromServer(f'Fetch TodayRecord StoreName ItemName price amount TotalPrice')
        if TodayRecordArray.size != 0:
            TodayRecordContent = pd.DataFrame(TodayRecordArray, columns=['StoreName', 'ItemName', 'price', 'amount', 'TotalPrice'])
            TodayStoreName = TodayRecordContent.at[0,'StoreName']
            TodayRecordContent = TodayRecordContent[['ItemName', 'price', 'amount', 'TotalPrice']]
        else:
            TodayRecordContent = pd.DataFrame()
            TodayStoreName = '無'
        return TodayStoreName, TodayRecordContent

    def setOrderComplete(self):
        set_msg = 'Copy HistoryRecord TodayRecord'
        self.setDataByServer(set_msg)
        set_msg = 'Clear TodayRecord'
        self.setDataByServer(set_msg)

    def checkTodayRecordbyDate(self, date):
        y, m, d = date.split('-')
        get_msg = f'Fetch TodayRecord StoreName:Year ({y})&Month ({m})&Day ({d})'
        storeNameArray = self.getDatafromServer(get_msg)
        if storeNameArray.size != 0:
            storeName = np.unique(storeNameArray.squeeze()).squeeze()
        else:
            storeName = ''
        return storeName
    def checkMenuRecordbyDate(self, date):
        y, m, d = date.split('-')
        get_msg = f'Fetch MenuRecord StoreName:Year ({y})&Month ({m})&Day ({d})'
        storeNameArray = self.getDatafromServer(get_msg)
        if storeNameArray.size != 0:
            storeName = np.unique(storeNameArray.squeeze()).squeeze()
        else:
            storeName = ''
        return storeName
    def getMenuDetailbyDate(self, date):
        y, m, d = date.split('-')
        get_msg = f'Fetch MenuDetail StoreName ItemName price:Year ({y})&Month ({m})&Day ({d})'
        menuArray = self.getDatafromServer(get_msg)
        if menuArray.size != 0:
            MenuContent = pd.DataFrame(menuArray, columns=['StoreName', 'ItemName', 'price'])
        else:
            MenuContent = pd.DataFrame()
        return MenuContent

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

    def deleteFavMenu(self,name):
        delete_msg = f'Delete FavMenu:FavMenuName ("{name}")'
        self.setDataByServer(delete_msg)
    
    




if __name__ == '__main__':
    client = clientHandler()
    
