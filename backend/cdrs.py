import json
import utils.auth as auth
from cdr.agentcdr import  get_single_cdr, update_single_cdr, insert_update_delete_customer
from utils.sanitize import sanitize_input
from utils.custom_exception import CustomError 
from config.database import Database


# import requests

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
           
            accpeted_http_methods = ['GET', 'POST','PUT']
            http_method = event['httpMethod']
            path_parameters = event['pathParameters']
            resource = event['resource']

            #    body = json.loads(event['body'])
            print(resource)
            if http_method not in accpeted_http_methods or http_method is None:
                raise CustomError("HTTP METHOD IS NOT ACCEPTED", http_status_code=403, details={"message": "HTTP METHOD IS NOT ACCEPTED"})
            
         
                                          
            if path_parameters :
                    # Strip HTML tags and escape HTML characters in one line
                    cdrtype = sanitize_input(path_parameters['cdrtype'])  
                    if cdrtype is None or cdrtype not in ['csdinbound','csdoutbound', 'collection','customer']:
                       raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "}) 
                                                                
                    match http_method:
                        case "GET":
                            cdr = ''
                            if cdrtype in ['csdinbound','csdoutbound', 'collection']: 
                                keys  = ['extension', 'getdate', 'starttimestamp']  
                                queryStringParameters = event['queryStringParameters'] 
                                
                                if queryStringParameters is not None and all(key in queryStringParameters for key in keys):  #check if startdate, enddate and tagname are in queryStringParameters then return true
                                    extension = sanitize_input(queryStringParameters['extension']) 
                                    starttimestamp = sanitize_input(queryStringParameters['starttimestamp']) 
                                    getdate = sanitize_input(queryStringParameters['getdate']) 
                                    cdr = get_single_cdr(cdrtype,extension,getdate,starttimestamp,cursor)
                                    
                                    return {
                                        "statusCode": 200,
                                        "headers": {
                                            "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                                            "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                                            "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                                        },                                     
                                        
                                        "body": json.dumps(cdr)
                                    }     
                                else:
                                    raise CustomError("query parameter are missing, invalid or incomplete..", http_status_code=404, details={"message": "query paramters are missing, invalid or incomplete.."})    

                            else:
                                raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "}) 
                          
                             
                        case "POST" | "PUT" | "DELETE":
                            if cdrtype == 'customer':
                              
                                queryStringParameters = event['queryStringParameters']
                         
                                if queryStringParameters  is  None or 'querytype' not in queryStringParameters or queryStringParameters['querytype']  not in ['update', 'insert','delete']:
                                   raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "}) 
                                    
                                body =  json.loads(event['body'])
                                querytype = queryStringParameters['querytype']
                                
                                print(querytype)
                 
                                print(body)
                                if body is None or not all(key in body for key in ['customer_id', 'customer_name','customer_number', 'updated_by']): 
                                 
                                   raise CustomError("Invalid or missing body parameters ", http_status_code=404, details={"message": "Invalid or missing body parameters"})
                             
                                customer_id = sanitize_input(body['customer_id'])
                                customer_name = sanitize_input(body['customer_name'])
                                customer_number = sanitize_input(body['customer_number'])
                                updated_by = sanitize_input(body['updated_by'])
                             
                                customer = insert_update_delete_customer(querytype, customer_id, customer_name, customer_number, updated_by,cursor,connection)
                                
                                if customer:
                                        return {                                    
                                            'statusCode': 201,
                                            "headers": {
                                                "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                                                "Access-Control-Allow-Methods": "POST,GET,OPTIONS,PUT,DELETE",
                                                "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                                             },                                             
                                            'body': json.dumps(True)
                                        }
                                else:
                                    raise CustomError("Cannot Insert or udpate customer records ", http_status_code=404, details={"message": "Cannot Insert or udpate customer records"})        
                                
                            else:
                                body = json.loads(event['body'])
                                print(body)
                                
                                
                                if body is not None and all(key in body for key in ['whoansweredcall','caller', 'getdate','starttimestamp', 'comment', 'commentby', 'tag']):
                                    getdate =  sanitize_input(body['getdate']) 
                                    starttimestamp = sanitize_input(body['starttimestamp']) 
                                    extension = sanitize_input(body['whoansweredcall']) 
                                    comment = sanitize_input(body['comment'])
                                    commentby = sanitize_input(body['commentby'])
                                    tag = sanitize_input(body['tag'])
                                    
                                    update_cdr = update_single_cdr(cdrtype, extension, getdate, starttimestamp,comment,commentby,tag,cursor,connection)
                                    return {                                    
                                            'statusCode': 201,
                                            "headers": {
                                                "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                                                "Access-Control-Allow-Methods": "POST,GET,OPTIONS,PUT,DELETE",
                                                "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                                             },                                             
                                            'body': json.dumps(update_cdr)
                                        }
                                else:
                                    raise CustomError("Invalid or missing body parameters ", http_status_code=404, details={"message": "Invalid or missing body parameters"})
            else:
                raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "})                        
                                                                 

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
