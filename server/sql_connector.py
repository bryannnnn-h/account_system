import pymysql
import logging
import numpy as np

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "4499tttt6688",
    "charset": "utf8mb4"
}

class db_connecter:
    def __init__(self):
        self.db_error = None
        self.conn = None
        self.db_logger, self.db_error_logger = self.createDBLogger()
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
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS TodayRecord (StoreName VARCHAR(20),StudentName VARCHAR(20), ItemName VARCHAR(20), price INT, amount INT, TotalPrice INT)')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS HistoryRecord (date VARCHAR(20), time VARCHAR(20), StoreName VARCHAR(20), StudentName VARCHAR(20), ItemName VARCHAR(20), price INT, amount INT, TotalPrice INT)')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS FavMenu (StoreName VARCHAR(20), FavMenuName VARCHAR(20), ItemName VARCHAR(20), price INT)')
            except Exception as ex:
                self.closeDB()
                self.db_error = ex
                self.db_error_logger.exception("Catch an exception when creating database or tables")
        except Exception as ex:
            self.db_error = ex
            self.db_error_logger.exception("Catch an exception when connecting to database")

    def closeDB(self):
        self.db_logger.debug('Closing database')
        self.conn.close()
    
    def createDBLogger(self):
        db_logger: logging.Logger = logging.getLogger(name='db')
        db_logger.setLevel(logging.DEBUG)
        db_error_logger: logging.Logger = logging.getLogger(name='dbError')
        db_error_logger.setLevel(logging.WARNING)
        
        formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        s_handler: logging.StreamHandler = logging.StreamHandler()
        f_handler: logging.FileHandler = logging.FileHandler(filename='dbLog.log', mode='w')
        s_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)
        db_logger.addHandler(s_handler)
        db_logger.addHandler(f_handler)

        f_error_handler: logging.FileHandler = logging.FileHandler(filename='dbErrorLog.log', mode='w')
        f_error_handler.setFormatter(formatter)
        db_error_logger.addHandler(s_handler)
        db_error_logger.addHandler(f_error_handler)
        return db_logger, db_error_logger

    def dbHandler(self, instruction):
        self.db_logger.debug(f'db execute {instruction}')
        instrcution_label = instruction.split(" ")[0]
        instruction_content = ' '.join(instruction.split(" ")[1:])
        try:
            if instrcution_label == "set": 
                setTable, setcol, setValue = instruction_content.split(' ') 
                sqlCommand = f'INSERT INTO {setTable} {setcol} VALUES {setValue}'[:-1]
                
                print(sqlCommand)
                self.db_cursor.execute(sqlCommand)
                self.conn.commit()

            elif instrcution_label == "Fetch":
                fetch_table = instruction_content.split(' ')[0]
                instruction_content = ' '.join(instruction_content.split(' ')[1:])
                if ':' in instruction_content:
                    fetch_column, fetch_condition = instruction_content.split(':')
                else:
                    fetch_column = instruction_content
                    fetch_condition = ''
                fetch_column = ','.join(fetch_column.split(' '))
                fetch_condition_msg = ''
                if len(fetch_condition) > 0:
                    fetch_condition_list = []
                    if '&' in fetch_condition:
                        fetch_condition_list = fetch_condition.split('&')
                    else:
                        fetch_condition_list.append(fetch_condition)
                    fetch_condition_msg += ' WHERE '
                    for i in fetch_condition_list:
                        column, cond = i.split(' ')
                        fetch_condition_msg += column
                        fetch_condition_msg += ' IN '
                        fetch_condition_msg += cond
                        if i != fetch_condition_list[-1]:
                            fetch_condition_msg += ' AND '
                self.db_cursor.execute(f'SELECT {fetch_column} FROM {fetch_table}{fetch_condition_msg}')
                result = np.array(self.db_cursor.fetchall())
                return result

            elif instrcution_label == "Clear":
                clearTable = instruction_content
                self.db_cursor.execute("TRUNCATE TABLE %s" % (clearTable))
                self.conn.commit()
            
            self.db_logger.debug(f'{instruction} success')
        except Exception as ex:
            self.db_error = ex
            self.db_error_logger.exception(f"Catch an exception when {instruction})")