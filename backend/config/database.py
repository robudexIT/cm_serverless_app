import pymysql
import pymysql.cursors
import time
import os
from dotenv import load_dotenv



#Load enviroment variables from .env file
load_dotenv()

connnection: dict 
cursor: dict

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']


# Connect to the database
connection = pymysql.connect(host= DB_HOST,
                             user= DB_USER,
                             password=DB_PASSWORD,
                             database=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

while True:
    try:
        connection = pymysql.connect(host='sbtphdb.cp6wc0kiikqz.us-east-1.rds.amazonaws.com',
                             user='sbtphadmin',
                             password='Kk0UyyRgFOQpehXBtGx6',
                             database='sbtphdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        print('Connecting to database is successful')
        break
    
    except Exception as error:
        print('Connection to database is failed')
        print("Error", error)
        time.sleep(5)
        
        
def connectDB():
    return {"connection": connection, "cursor": cursor}
        