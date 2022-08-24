import socket
from client.client_config import *
import sys
import pandas as pd

class clientHandler:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IP, PORT))
    def sendData(self, msg):
        self.sock.sendall(msg.encode())
        response = str(self.sock.recv(1024).decode())
        print("Received: {}".format(response))

    def setTodayMenu(self, df):
        self.sock.sendall('Clear TodayMenu'.encode('utf-8'))
        self.sock.recv(1024)
        self.sock.sendall('Clear TodayRecord'.encode('utf-8'))
        self.sock.recv(1024)
        for index, item in df.iterrows():
            self.sock.sendall(('setTodayMenu %s %s %s' % (item['StoreName'], item['ItemName'], item['price'])).encode('utf-8'))
            self.sock.recv(1024)


if __name__ == '__main__':
    client = clientHandler()
    
