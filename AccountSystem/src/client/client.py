import socket
from client.client_config import *
import sys
import pandas as pd
import struct

class clientHandler:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IP, PORT))
        self.sock.sendall('accountSystem'.encode())
        self.sock.recv(1024)

    def setTodayMenu(self, df):
        self.setDataByServer('Clear TodayMenu')

        todayMsg = 'set TodayMenu (StoreName,ItemName,price) '
        for index, item in df.iterrows():
            todayMsg += f'(\"{item["StoreName"]}\",\"{item["ItemName"]}\",{int(item["price"])}),'

        self.setDataByServer(todayMsg)

    def addFavMenu(self, df):   
        FavMsg = 'set FavMenu (StoreName,FavMenuName,ItemName,price) '
        for index, item in df.iterrows():
            FavMsg += f'(\"{item["StoreName"]}\","{item["FavMenuName"]}\",\"{item["ItemName"]}\",{int(item["price"])}),'
        self.setDataByServer(FavMsg)

    def setDataByServer(self, sendDataMsg):
        self.sock.sendall('SetData'.encode())
        #self.sock.recv(1024)
        sendDataMsg = sendDataMsg.encode()
        byte_len = struct.pack("i", len(sendDataMsg))            
        self.sock.sendall(byte_len)
        #self.sock.recv(1024)
        self.sock.sendall(sendDataMsg)
        self.sock.recv(1024) #server recieved done
        self.sock.recv(1024) #db_handler signal success



if __name__ == '__main__':
    client = clientHandler()
    
