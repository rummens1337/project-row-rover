from src.common.log import *
import pymysql.cursors

class Column:

    name = ""
    value = ""

    def __init__(self, name, value=""):
        self.name = name
        self.value = value

    def getName(self):
        return self.name

    def getValue(self):
        return self.value


class Database:

    def __init__(self):

        # Connect to the database
        self.connection = pymysql.connect(host='localhost',
                                     user='daviddb',
                                     password='HRvu4CX5',
                                     db='david',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    def insert(self, table, columns):
        pass


    def select(self, table, columns, joins = [], where = ""):
        sql = "SELECT "
        
        sep = ""
        for i in range(len(columns)):
            sql += sep + "`" + table + "_" + str(columns[i].getName()) + "`"
            sep = ", "

        sql += " FROM `" + table + "`"
        
        for i in range(len(joins)):
            sql += " JOIN `" + joins[i][0] + "` ON " + joins[i][1]

        if(where):
            sql += " WHERE " + where

        sql += ";"

        with self.connection.cursor() as cursor:
            # Read a single record
            cursor.execute(sql)
            result = cursor.fetchall()
            return result


    def insertTest(self):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()

            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                print(result)
        finally:
            self.connection.close()
