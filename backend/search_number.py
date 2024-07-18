import json
from cdr.agentcdr import get_search_number
import utils.auth as auth
from utils.sanitize import sanitize_input
from utils.custom_exception import CustomError
from config.database import Database


def lambda_handler(event, context):
    try:
        db = None 
        if event['httpMethod'] == 'OPTIONS':
               return {
                     'statusCode': 200,
                     'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS,PUT,DELETE',
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
            search_type = sanitize_input(path_parameters.get('search_type'))             
        
            if  queryStringParameters is not None and 'customer_number'  in queryStringParameters and search_type is not None and search_type in ['customer','collectiondetails','csdinbounddetails', 'csdoutbounddetails']:
                customer_number = sanitize_input(queryStringParameters['customer_number']) 
                search_result = get_search_number(customer_number, search_type,cursor)
                return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                    "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                },                     
                 "body": json.dumps(search_result)
                }
            else:
              raise CustomError("Invalid or missing parameters", http_status_code=403, details={"message": "Invalid or missing parameters"})       
           
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})
                          
   
    except CustomError as e:
        return {
            "statusCode": e.http_status_code, 
             "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
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
               "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
            },                 
            'body': json.dumps(f'Error: {str(e)}')
        }
    finally:
        if db:
          db.close()   
       

