from server import ThreadedTCPServer, ThreadedTCPRequestHandler
from server_config import HOST, PORT

if __name__ == '__main__':
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.closeServer()