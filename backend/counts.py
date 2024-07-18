import json
import utils.auth as auth
import config.database as database 
from utils.custom_exception import CustomError 
from utils.sanitize import sanitize_input
from datetime import datetime
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
            if event['pathParameters'] and 'count' in event['pathParameters']:
                path_parameters = event['pathParameters']
                count = sanitize_input(path_parameters.get('count')) 
                if count == 'cdr':
                    
                    data = []
                    getdate = datetime.now().strftime('%Y-%m-%d')
                    #get active agents
                    query = """SELECT COUNT(*) as active_agents FROM csd_agents WHERE receive_calls=1"""   
                    cursor.execute(query)
                    active_agents = cursor.fetchone()
                    
                    data.append({
                        'active_agents': active_agents['active_agents']
                    })
                  
                    # data.append({'active_agents': active_agents['active_agents']}) 
                    # return data
                    #get active agents
                    query = """SELECT COUNT(*) as inactive_agents FROM csd_agents WHERE receive_calls=0"""
                    cursor.execute(query)
                    inactive_agents = cursor.fetchone()
                    
                    data.append({'inactive_agents': inactive_agents['inactive_agents']})
                    
     
                
                    #summaries    
                    csdinboundsummaries = """SELECT COUNT(*) FROM csd_inbound_cdr WHERE getDate=%s"""
                    csdoutboundsummaries = """SELECT COUNT(*) FROM csd_outbound_cdr WHERE getDate=%s"""
                    collectionsummaries = """SELECT COUNT(*) FROM collection_outbound_cdr WHERE getDate=%s"""
                    salessummaries = """SELECT COUNT(*) FROM sales_outbound_cdr WHERE getDate=%s"""
                    missedcallssummaries = """SELECT COUNT(*) FROM csd_inbound_cdr WHERE getDate=%s AND CallStatus!='ANSWER'"""
                    
                    queries = [{'csdinboundsummaries': csdinboundsummaries}, {'csdoutboundsummaries': csdoutboundsummaries}, {'collectionsummaries': collectionsummaries}, {'missedcallssummaries': missedcallssummaries}]

                    for query in queries:
                        for key, value in query.items():  
                           cursor.execute(value,(getdate,))
                           counts = cursor.fetchone()
                           data.append({key: counts['COUNT(*)']})
                        
                    return {
                        'statusCode': 200,
                        "headers": {
                           "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                           "Access-Control-Allow-Methods": "POST,GET,PUT,OPTIONS",
                           "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                       },                             
                        'body': json.dumps(data)
                    }
                
                #count total registered customers..   
                elif count == 'customer':
                    cursor.execute("""SELECT COUNT(*) AS customer_count FROM customer_info""")
                    customer = cursor.fetchone()
                    return {
                        'statusCode': 200,
                        "headers": {
                           "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                           "Access-Control-Allow-Methods": "POST,GET,PUT,OPTIONS",
                           "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                       },                             
                        'body': json.dumps({ "customer_registered_count" : customer['customer_count']}) 
                    }
                else:
                  raise CustomError("Invalid path parameter", http_status_code=403, details={"message": "Invalid path parameter"})      
            else:
                raise CustomError("Path Parameters are missing", http_status_code=403, details={"message": "Path Parameters are missing"})
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})
                          
   
    except CustomError as e:
        return {
            "statusCode": e.http_status_code, 
             "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                "Access-Control-Allow-Methods": "POST,GET,PUT,OPTIONS",
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
                "Access-Control-Allow-Methods": "POST,GET,PUT,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
             },                 
            'body': json.dumps(f'Error: {str(e)}')
        }
    finally:
        if db:
          db.close()
    