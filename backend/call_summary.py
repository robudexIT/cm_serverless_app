import json
from cdr.agentcdr import get_call_summary
import utils.auth as auth
from utils.sanitize import sanitize_input
from datetime import datetime
from config.database import Database
from utils.custom_exception import CustomError 

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

startdate = ''
enddate = ''
tagname = ''

agents_cdrs = ''

def lambda_handler(event, context):
   db = None 
   try:
        if event['httpMethod'] == 'OPTIONS':
               return {
                     'statusCode': 200,
                     'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                     },
                     'body': ''
               }

        db = Database()
        connection_details = db.get_connection()
        connection = connection_details['connection']
        cursor = connection_details['cursor']
        headers = event.get('headers', {})
        verify = auth.verify_access_token(headers) 
 
   
        if verify:
        
            queryStringParameters = event['queryStringParameters']
            path_parameters = event['pathParameters']
            callsummaries = sanitize_input(path_parameters.get('callsummaries')) 
            #callsummaries expect this one of this values csdinbound, csdoutbound, collection
            match callsummaries:
               case "csdinbound":
                  keys  = ['startdate', 'enddate', 'tagname']
                  # print(callsummaries) 
                  # if all(key in queryStringParameters for key in keys):  #check if startdate, enddate and tagname is queryStringParameters  return true if all keys are there
                  if queryStringParameters is not None and all(key in queryStringParameters for key in keys): 
                     startdate = sanitize_input(queryStringParameters['startdate']) 
                     enddate = sanitize_input(queryStringParameters['enddate']) 
                     tagname = sanitize_input(queryStringParameters['tagname']) 
                     
                  else:
                     startdate = datetime.now().strftime('%Y-%m-%d')
                     enddate = datetime.now().strftime('%Y-%m-%d')
                     tagname = "all"

                  agents_cdrs = get_call_summary(startdate, enddate, "", "",tagname, "", "", callsummaries, f"{callsummaries}details", False, cursor)  
                                     
               case "csdoutbound" | "collection":
                  print('it cam here')
                  keys = ['startdate', 'enddate', 'tagname', 'duration', 'direction']
                  if queryStringParameters is not None and all(key in queryStringParameters for key in keys):
                     startdate = sanitize_input(queryStringParameters['startdate']) 
                     enddate = sanitize_input( queryStringParameters['enddate'])
                     tagname = sanitize_input(queryStringParameters['tagname'])
                     duration = sanitize_input(queryStringParameters['duration']) 
                     direction = sanitize_input(queryStringParameters['direction'])                      
                  else:
                     startdate = datetime.now().strftime('%Y-%m-%d')
                     enddate = datetime.now().strftime('%Y-%m-%d')
                     tagname = "all"  
                     duration = "0"
                     direction = "UP"                    
                  agents_cdrs = get_call_summary(startdate, enddate, "", "", tagname, duration, direction, callsummaries, f"{callsummaries}details", False,cursor)
               case "sales":
                  pass
               case "missedcalls":
                  keys = ['startdate', 'enddate']
                  
                  if queryStringParameters is not None and all(key in queryStringParameters for key in keys): 
                    
                     startdate = sanitize_input(queryStringParameters['startdate']) 
                     enddate = sanitize_input(queryStringParameters['enddate'] ) 
                  else:
                     startdate = datetime.now().strftime('%Y-%m-%d')
                     enddate = datetime.now().strftime('%Y-%m-%d')                     
                  agents_cdrs = get_call_summary(startdate, enddate, "", "", "", "", "", callsummaries, f"{callsummaries}details", False, cursor)                   
               case _:
                  raise CustomError("Invalid Parameters", http_status_code=403, details={"message": "Invalid Parameters"})
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                    "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin,Access-Control-Allow-Methods"
                },                
                 "body": json.dumps(agents_cdrs)
            }
            
  
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})
                          
   
   except CustomError as e:
        return {
            "statusCode": e.http_status_code, 
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                    "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin,Access-Control-Allow-Methods"
                },            
            'body': json.dumps(f'Error: {str(e)}')
        }
   #Catch All Error
   except Exception as e:

       return {
          
            "statusCode": 500, # json.loads(error)['http_status_code'],
            "headers": {
                    "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                    "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin,Access-Control-Allow-Methods"
             },            
            
            'body': json.dumps(f'Error: {str(e)}')
        }
   finally:
      if db:
         db.close()   