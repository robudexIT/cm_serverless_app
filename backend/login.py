import json
import pymysql
import bcrypt
import os
from jose import jwt
from dotenv import load_dotenv
from config.database import Database
import utils.auth as auth
from utils.sanitize import sanitize_input
from datetime import datetime, timedelta


def lambda_handler(event, context):
    
    db = Database()
    connection_details = db.get_connection()
    connection = connection_details['connection']
    cursor = connection_details['cursor']
    
    try:
     
        body = json.loads(event['body'])
        extension = sanitize_input(body['extension']) 
        secret = sanitize_input( body['secret'])
        csd_agent = 0
        agentcalltype = ""
        collection_agent = 0
        blended = "0"
      
        cursor.execute("SELECT * FROM login WHERE extension=%s ", (extension,))
        
        user = cursor.fetchone()
      
        if user and user['secret'] == secret:
            cursor.execute("""SELECT * FROM calltype WHERE extension=%s""", (extension,))
            calltype = cursor.fetchone()
            
            cursor.execute("""SELECT COUNT(*) FROM csd_agents WHERE extension=%s""", (extension,))
            csd_agent = cursor.fetchone()
            
            cursor.execute("""SELECT COUNT(*) FROM collection_agents WHERE extension=%s""", (extension,))
            collection_agent = cursor.fetchone()
            
            print(csd_agent)
            print(collection_agent) 
            
    
            
          
            if csd_agent['COUNT(*)'] == 1 and collection_agent['COUNT(*)'] == 1 :
                blended = "1"
            
            if calltype :
                agentcalltype = calltype['calltype']
                    
            
            payload = {
            'data': {
                'extension': user['extension'],
                'name': user['name'],
                'position': user['position'],
                'blended': blended,
                'calltype': agentcalltype
            }
            
          
            }
            token = auth.create_access_token(payload)
            print(token)
            return {
                'statusCode': 200,
                
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                    "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                },
                'body': json.dumps({'jwt': token, 'message': "Successful login" })
            }
        else:
            return {
                'statusCode': 401, 
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                    "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization"
                },                
                'body': json.dumps({'message': 'User Not exist or Invalid Passowrd'})
            }    
        
    except Exception as e:
        return {
            "statusCode":  500,
            'body': json.dumps(f'Error: {str(e)}')
        }
    finally:
        db.close()

# user = lambda_handler()

# print(user)

