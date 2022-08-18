import pymysql

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
        except Exception as ex:
            self.db_error = ex
            

    def closeDB(self):
        self.conn.close()

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