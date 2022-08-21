from distutils.log import Log
import sys, msvcrt
from tim_server import ThreadedTCPServer, ThreadedTCPRequestHandler
from server_config import HOST, PORT
from tim_sql_connector import db_connecter

if __name__ == '__main__':
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.closeServer()
    