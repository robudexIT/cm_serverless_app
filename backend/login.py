import json
import pymysql
import bcrypt
import os
from jose import jwt
from dotenv import load_dotenv
import config.database as database 
import utils.auth as auth
from datetime import datetime, timedelta


#Load environment variable from .env file
load_dotenv()

# import requests


db = database.connectDB()
connection = db['connection']
cursor = db['cursor']

def lambda_handler(event, context):

    try: 
        body = json.loads(event['body'])
        extension = body['extension']
        secret = body['secret']
        
        cursor.execute("SELECT * FROM login WHERE extension=%s ", (extension))
        
        user = cursor.fetchone()
        
        if user and user['secret'] == secret:
        
            payload = {
            'data': {
                'extension': user['extension'],
                'name': user['name'],
                'position': user['position']
            }
            
          
            }
            token = auth.create_access_token(payload)
            return {
                'statusCode': 200,
                'body': json.dumps({'jwt': token, 'message': "Successful login" })
            }
        else:
            return {
                'statusCode': 401, 
                'body': json.dumps({'message': 'User Not exist or Invalid Passowrd'})
            }    
        
    except Exception as e:
        return {
            "statusCode": 500,
            'body': json.dumps(f'Error: {str(e)}')
        }


# user = lambda_handler()

# print(user)

