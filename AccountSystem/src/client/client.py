import socket
from client.client_config import *
import sys
import pandas as pd

class clientHandler:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IP, PORT))
        self.sock.sendall('accountSystem'.encode())
        self.sock.recv(1024)

    def setTodayMenu(self, df):
        self.sock.sendall('SetData'.encode())
        self.sock.recv(1024) 
        sendDataMsg = 'Clear TodayMenu'
        self.sock.sendall(str(len(sendDataMsg)).encode())
        self.sock.recv(1024)
        self.sock.sendall(sendDataMsg.encode('utf-8'))
        self.sock.recv(1024)

        self.sock.sendall('SetData'.encode())
        self.sock.recv(1024)
        sendDataMsg = 'set TodayMenu (StoreName,ItemName,price) '
        for index, item in df.iterrows():
            sendDataMsg += f'(\"{item["StoreName"]}\",\"{item["ItemName"]}\",{int(item["price"])}),'

        self.sock.sendall(str(len(sendDataMsg)).encode())
        self.sock.recv(1024)
        self.sock.sendall(sendDataMsg.encode('utf-8'))
        self.sock.recv(1024)

    def addFavMenu(self, df):
        self.sock.sendall('SetData'.encode())
        self.sock.recv(1024)
        sendDataMsg = 'set FavMenu (StoreName,FavMenuName,ItemName,price) '
        for index, item in df.iterrows():
            sendDataMsg += f'(\"{item["StoreName"]}\","{item["FavMenuName"]}\",\"{item["ItemName"]}\",{int(item["price"])}),'
            
        self.sock.sendall(str(len(sendDataMsg)).encode())
        self.sock.recv(1024)
        self.sock.sendall(sendDataMsg.encode('utf-8'))
        self.sock.recv(1024)


if __name__ == '__main__':
    client = clientHandler()
    
