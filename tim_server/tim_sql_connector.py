from stat import filemode
import pymysql
import logging

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "4499tttd6688",
    "charset": "utf8mb4"
}

class db_connecter:
    def __init__(self):
        self.db_error = None
        self.conn = None
        self.db_logger = self.createDBLogger()
        self.DBconnection()

    def DBconnection(self):
        try:
            self.conn = pymysql.connect(**db_settings)
            try:
                self.db_cursor = self.conn.cursor()
                self.db_cursor.execute('CREATE DATABASE IF NOT EXISTS ernies_db DEFAULT CHARACTER SET utf8mb4')
                self.db_cursor.execute('USE ernies_db')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS basic_info (id INT, name VARCHAR(20), grade INT, program VARCHAR(20), price INT)')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS TodayMenu (StoreName VARCHAR(20), ItemName VARCHAR(20), price INT)')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS TodayRecord (StudentName VARCHAR(20), ItemName VARCHAR(20), price INT, amount INT)')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS HistoryRecord (date VARCHAR(20), time VARCHAR(20), StudentName VARCHAR(20), ItemName VARCHAR(20), price INT, amount INT)')
            except Exception as ex:
                self.closeDB()
                self.db_error = ex
                self.db_logger.exception("Catch an exception when creating database or tables")
        except Exception as ex:
            self.db_error = ex
            self.db_logger.exception("Catch an exception when connecting to database")

    def closeDB(self):
        self.conn.close()
    
    def createDBLogger(self):
        db_logger: logging.Logger = logging.getLogger(name='db')
        db_logger.setLevel(logging.WARNING)
        
        s_handler: logging.StreamHandler = logging.StreamHandler()
        f_handler: logging.FileHandler = logging.FileHandler(filename='dbErrorLog.log', mode='w')
        formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        s_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)
        db_logger.addHandler(s_handler)
        db_logger.addHandler(f_handler)
        return db_logger

    def dbHandler(self, instruction):
        instrcution_label = instruction.split(" ")[0]
        instruction = ' '.join(instruction.split(" ")[1:])
        if instrcution_label == "setTodayMenu":
            storename, itemname, price = instruction.split(' ')
            self.db_cursor.execute('INSERT INTO TodayMenu VALUES("%s", "%s", %d)' % (storename, itemname, int(price)))
            self.conn.commit()

        elif instrcution_label == "Clear":
            clearTable = instruction
            self.db_cursor.execute("TRUNCATE TABLE %s" % (clearTable))
            self.conn.commit()