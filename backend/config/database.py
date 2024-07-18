import pymysql
import pymysql.cursors
import time
import os
import mysql.connector
from dotenv import load_dotenv



#Load enviroment variables from .env file
load_dotenv()

connnection: dict 
cursor: dict

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']


class Database:
    def __init__(self):
        self.host = DB_HOST
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.database = DB_NAME
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
            try:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                self.cursor = self.connection.cursor(dictionary=True)
                print("Connecting to database is successful")
            except Exception as error:
                print("Connection to database failed")
                print("Error:", error)
                time.sleep(5)

    def get_connection(self):
        return {"connection": self.connection, "cursor": self.cursor}

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed")



