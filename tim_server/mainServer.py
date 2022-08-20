from distutils.log import Log
import sys, msvcrt
from tim_server import ThreadedTCPServer, ThreadedTCPRequestHandler
from server_config import HOST, PORT
from tim_sql_connector import db_connecter

if __name__ == '__main__':
    '''
    try:
        db = db_connecter()
        if db.db_error:
            raise
        else:
            print("Database connect success")
    except:
        print(f"與資料庫連線時發生錯誤：{db.db_error}\n請排除錯誤後重新開啟伺服器")
        print("按任意鍵關閉...")
        msvcrt.getch()
        sys.exit(0)
    '''
    db = db_connecter()
    if db.db_error:
        print(f"與資料庫連線時發生錯誤，請排除錯誤後重新開啟伺服器")
        print("按任意鍵關閉...")
        msvcrt.getch()
        sys.exit(0)


    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler, db=db)
    print('server start at: %s:%s' % (HOST, PORT))


    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('server shutdown')
        sys.exit(0)
    finally:
        print('close database')
        db.closeDB()
    