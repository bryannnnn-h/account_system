from re import I
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

    def clearTable(self, TableName):
        self.setDataByServer(f'Clear {TableName}')

    def TodayCopy2History(self):
        self.setDataByServer('Copy HistoryRecord TodayRecord')
    '''
    def setMenuDetail(self, y, m, d, df):
        self.setDataByServer(f'Delete MenuDetail:Year ({y})&Month ({m})&Day ({d})')
        todayMsg = 'set MenuDetail (Year,Month,Day,StoreName,ItemName,price) '
        for index, item in df.iterrows():
            todayMsg += f'({y},{m},{d},\"{item["StoreName"]}\",\"{item["ItemName"]}\",{int(item["price"])}),'

        self.setDataByServer(todayMsg)
    '''
    def getSelectedMenuInfo(self):
        get_msg = 'Fetch MenuRecord ID Year Month Day StoreName:isSelected (True)'
        MenuInfo = self.getDatafromServer(get_msg)
        if MenuInfo.size != 0:
            MenuInfo = MenuInfo.squeeze()
        else:
            menuID = '0'
            menuDate = ''
            storeName = '無'
        return menuID, menuDate, storeName
    def updateMenuState(self, menuID, Complete=False):
        set_msg = f'Update MenuRecord isSelected False&isCompleted {Complete}:ID ({menuID})'
        self.setDataByServer(set_msg)
    
    def setMenu(self, y, m, d, storeName, df):
        delete_id = self.getDatafromServer(f'Fetch MenuRecord ID:Year ({y})&Month ({m})&Day ({d})&isCompleted (False)').squeeze()
        if delete_id:
            self.setDataByServer(f'Delete MenuDetail:ID ({delete_id})')
            self.setDataByServer(f'Delete MenuRecord:ID ({delete_id})')
        set_msg = f'set MenuRecord (Year,Month,Day,StoreName,isSelected,isCompleted) ({y},{m},{d},"{storeName}",False,False)'
        self.setDataByServer(set_msg)
        insert_id = self.getDatafromServer(f'Fetch MenuRecord ID:Year ({y})&Month ({m})&Day ({d})&isCompleted (False)').squeeze()
        todayMsg = 'set MenuDetail (ID,ItemName,price) '
        for index, item in df.iterrows():
            todayMsg += f'({insert_id},\"{item["ItemName"]}\",{int(item["price"])}),' 
        self.setDataByServer(todayMsg)
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
        if TableArray.size:
            TableContent = pd.DataFrame(TableArray, columns=columnArray)
        else:
            TableContent = pd.DataFrame([['']*len(columnArray)], columns=columnArray)
            #TableContent = pd.DataFrame(columns=columnArray)
        return TableContent

    def deleteTablebyId(self, TableName, id):
        idMsg = f'{id}'.replace("[", "(").replace("]", ")").replace(" ", "")
        msg = f'Delete {TableName}:ID {idMsg}'
        self.setDataByServer(msg)

    def InsertAccountTable(self, TableName, data):
        TypeArray = self.getDatafromServer(f'showInfo DATA_TYPE {TableName}')[1:]

        col_msg = f'{list(data.columns)}'.replace("[", "(").replace("]", ")").replace(" ","").replace("'", "")
        
        data_msg = ''

        for index, item in data.iterrows():
            item_msg = ''
            if len(TypeArray) == len(item):
                for i, dtype in enumerate(TypeArray):
                    print('dtype is ', dtype)
                    if dtype == 'varchar':
                        item_msg += f"'{item[i]}'"
                    else:
                        item_msg += f"{item[i]}"
                    if i != len(TypeArray)-1:
                        item_msg += ','       
            data_msg += f'({item_msg}),'

        
        msg = f'set {TableName} {col_msg} {data_msg}'
        print(msg)
        
        self.setDataByServer(msg)
           

    def InsertRelevantTable(self, TableName, df):
        TypeArray = self.getDatafromServer(f'showInfo column_name,DATA_TYPE {TableName}')
        pass


    def UpdateAccountTable(self, TableName, action, id, column, data):
        TypeArray = self.getDatafromServer(f'showInfo DATA_TYPE {TableName}')[1:]
        msg = f'{action} {TableName} '
        for i in range(len(column)):
            if TypeArray[i] == 'varchar':
                msg += f"{column[i]} '{data[i]}'"
            else:
                msg += f'{column[i]} {data[i]}'
            if i != len(column) - 1:
                msg += '&'
            else:
                msg += ':'
        msg += f'ID ({id})'
        print(msg)
        self.setDataByServer(msg)

    def getTodayRecord(self):
        TodayRecordArray = self.getDatafromServer(f'Fetch TodayRecord ItemName price amount TotalPrice')
        if TodayRecordArray.size != 0:
            TodayRecordContent = pd.DataFrame(TodayRecordArray, columns=['ItemName', 'price', 'amount', 'TotalPrice'])
        else:
            TodayRecordContent = pd.DataFrame()
        return TodayRecordContent

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
        get_msg = f'Fetch MenuRecord ID StoreName:Year ({y})&Month ({m})&Day ({d})&isCompleted (False)'
        ID_storeNameArray = self.getDatafromServer(get_msg)
        if ID_storeNameArray.size != 0:
            id, storeName = ID_storeNameArray.squeeze()
        else:
            storeName = ''
            id = ''
        return id, storeName
    def getMenuDetailbyID(self, id):
        get_msg = f'Fetch MenuDetail ItemName price:ID ({id})'
        menuArray = self.getDatafromServer(get_msg)
        if menuArray.size != 0:
            MenuContent = pd.DataFrame(menuArray, columns=['ItemName', 'price'])
        else:
            MenuContent = pd.DataFrame()
        return MenuContent
    def getMenuRecord(self):
        get_msg = f'Fetch MenuRecord *'
        menuRecordArray = self.getDatafromServer(get_msg)
        menuRecordColumn = self.getDatafromServer('showColumn MenuRecord')
        if menuRecordArray.size != 0:
            menuRecordData = pd.DataFrame(menuRecordArray, columns=menuRecordColumn)
        else:
            menuRecordData = pd.DataFrame([['']*len(menuRecordColumn)], columns=menuRecordColumn)
        return menuRecordData
        
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
    
