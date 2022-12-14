import pymysql
import logging
import numpy as np
from db_settings import db_settings

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
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS basic_info (ID INT NOT NULL AUTO_INCREMENT, name VARCHAR(20) NOT NULL, grade VARCHAR(20) NOT NULL, program INT, tel VARCHAR(20), 備註 VARCHAR(200), PRIMARY KEY(ID))')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS AccountTable (ID INT, Year INT, Month INT, name VARCHAR(20) NOT NULL, grade VARCHAR(20) NOT NULL, program INT, foodExpense INT, bookExpense INT, Total INT, isPaid BOOL DEFAULT FALSE, 備註 VARCHAR(200))')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS FoodExpenseDetail (ID INT, Year INT, Month INT, Day INT, name VARCHAR(20) NOT NULL, grade VARCHAR(20) NOT NULL, price INT DEFAULT 0, isCounted BOOL DEFAULT FALSE, 備註 VARCHAR(200))')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS BookExpenseDetail (ID INT, Year INT, Month INT, name VARCHAR(20) NOT NULL, grade VARCHAR(20) NOT NULL, price INT DEFAULT 0, isCounted BOOL DEFAULT FALSE, 備註 VARCHAR(200))')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS MenuDetail (ID INT, ItemName VARCHAR(20) NOT NULL, price INT NOT NULL)')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS MenuRecord (ID INT NOT NULL AUTO_INCREMENT, Year INT NOT NULL, Month INT NOT NULL, Day INT NOT NULL, StoreName VARCHAR(20) NOT NULL, isSelected BOOL DEFAULT FALSE, isCompleted BOOL DEFAULT FALSE, PRIMARY KEY(ID))')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS TodayRecord (Student_ID INT, Menu_ID INT, Year INT, Month INT, Day INT, StoreName VARCHAR(20),StudentName VARCHAR(20), ItemName VARCHAR(20), price INT, amount INT, TotalPrice INT)')
                self.db_cursor.execute('CREATE TABLE IF NOT EXISTS HistoryRecord (Student_ID INT, Menu_ID INT, Year INT, Month INT, Day INT, StoreName VARCHAR(20), StudentName VARCHAR(20), ItemName VARCHAR(20), price INT, amount INT, TotalPrice INT)')
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
                sqlCommand = f'INSERT INTO {setTable} {setcol} VALUES {setValue}'
                if sqlCommand[-1] == ',':
                    sqlCommand = sqlCommand[:-1]
                self.db_cursor.execute(sqlCommand)
                self.conn.commit()

            elif instrcution_label == "Fetch":
                #'Fetch_Table Fetch_ColumnA Fetch_ColumnB ...:cond_columnA (condA)&cond_columnB (condB)&...'
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

            elif instrcution_label == 'showColumn':
                fetch_table = instruction_content
                self.db_cursor.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{fetch_table}' order by ORDINAL_POSITION")
                result = np.array(self.db_cursor.fetchall()).squeeze()
                return result

            elif instrcution_label == 'showInfo':
                fetchInfo, fetch_table = instruction_content.split(' ')
                self.db_cursor.execute(f"SELECT {fetchInfo} FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{fetch_table}' order by ORDINAL_POSITION")
                if ',' not in fetchInfo:
                    result = np.array(self.db_cursor.fetchall()).squeeze()
                else:
                    result = np.array(self.db_cursor.fetchall())
                return result

            elif instrcution_label == "Clear":
                clearTable = instruction_content
                self.db_cursor.execute("TRUNCATE TABLE %s" % (clearTable))
                self.conn.commit()
            
            elif instrcution_label == "Delete":
                #'del_table:del_column1 (del_val1,delval2,...)&del_column2 (del_val1,delval2,...)&...'
                if ':' in instruction_content: 
                    del_table, del_cond = instruction_content.split(':')
                else:
                    del_table = instruction_content
                    del_cond = ''
                del_condition_msg = ''
                if len(del_cond) > 0:
                    del_cond_list = []
                    if '&' in del_cond:
                        del_cond_list = del_cond.split('&')
                    else:
                        del_cond_list.append(del_cond)
                    del_condition_msg += ' WHERE '
                    for i in del_cond_list:
                        column, val = i.split(' ')
                        del_condition_msg += column
                        del_condition_msg += ' IN '
                        del_condition_msg += val
                        if i != del_cond_list[-1]:
                            del_condition_msg += ' AND '
                self.db_cursor.execute(f'DELETE FROM {del_table}{del_condition_msg}')
                self.conn.commit()
            elif instrcution_label == 'Copy':
                target, source = instruction_content.split(' ')
                target_table = target 
                target_column = ''
                source_table = source 
                source_column = '*'
                if ':' in target:
                    target_table, target_column = target.split(':')
                if ':' in source:
                    source_table, source_column = source.split(':')
                self.db_cursor.execute(f'INSERT {target_table}{target_column} SELECT {source_column} FROM {source_table}')
                self.conn.commit()
            elif instrcution_label == 'Update':
                #'update_table update_column1 update_value1&...:cond_column1 (cond_val1,cond_val2,...)&cond_column2 (cond_val1,cond_val2,...)&...'
                update_table = instruction_content.split(' ')[0]
                instruction_content = ' '.join(instruction_content.split(' ')[1:])
                if ':' in instruction_content: 
                    update_column_val, update_cond = instruction_content.split(':')
                else:
                    update_column_val = instruction_content
                    update_cond = ''
                update_msg = ''
                update_list = []
                if '&' in update_column_val:
                    update_list = update_column_val.split('&')
                else:
                    update_list.append(update_column_val)
                for i in update_list:
                    column, val = i.split(' ')
                    update_msg += f'{column}={val}'
                    if i != update_list[-1]:
                        update_msg += ','
                update_condition_msg = ''
                if len(update_cond) > 0:
                    update_cond_list = []
                    if '&' in update_cond:
                        update_cond_list = update_cond.split('&')
                    else:
                        update_cond_list.append(update_cond)
                    update_condition_msg += ' WHERE '
                    for i in update_cond_list:
                        column, val = i.split(' ')
                        update_condition_msg += column
                        update_condition_msg += ' IN '
                        update_condition_msg += val
                        if i != update_cond_list[-1]:
                            update_condition_msg += ' AND '
                self.db_cursor.execute(f'UPDATE {update_table} SET {update_msg}{update_condition_msg}')
                self.conn.commit()
            self.db_logger.debug(f'{instruction} success')
        except Exception as ex:
            self.db_error = ex
            self.db_error_logger.exception(f"Catch an exception when {instruction})")