import json
from datetime import datetime
from config import database 
from utils import auth

# import requests

startdate = ''
enddate = ''
tagname = ''

db = database.connectDB()
connection = db['connection']
cursor = db['cursor'] 

# import requests


def lambda_handler(event, context):
   try:
        headers = event.get('headers', {})
        verify = auth.verify_access_token(headers) 
        
        if verify:
        
            queryStringParameters = event['queryStringParameters']
              #check if startdate, enddate and tagname is queryStringParameters 
            keys  = ['startdate', 'enddate', 'tagname']
            
            if all(key in queryStringParameters for key in keys):
                startdate =  queryStringParameters['startdate']
                enddate = queryStringParameters['enddate']
                tagname = queryStringParameters['tagname']
            else:
                startdate = datetime.now().strftime('%Y-%m-%d')
                enddate = datetime.now().strftime('%Y-%m-%d')
                tagname = "all"
            
            cursor.execute("SELECT * FROM csdinbound")
            
            agents = cursor.fetchall()
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "agents": agents,
                    # "location": ip.text.replace("\n", "")
                }),
            }
        else:
            raise Exception('Not Authorized')
 

   except Exception as e:
        return {
            "statusCode": 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
