import json
import utils.auth as auth
import agent.agent as agent
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
           
            accpeted_http_methods = ['GET', 'POST','PUT','DELETE']
            http_method = event['httpMethod']
            path_parameters = event['pathParameters']
            resource = event['resource']

            #    body = json.loads(event['body'])
            print(resource)
            if http_method not in accpeted_http_methods or http_method is None:
                raise CustomError("HTTP METHOD IS NOT ACCEPTED", http_status_code=403, details={"message": "HTTP METHOD IS NOT ACCEPTED"})
            
         
            
            if  resource == "/api/agents/csd/inbound_group"  and event['queryStringParameters'] and 'group' in event['queryStringParameters']:
                queryStringParameters = event['queryStringParameters']
                group = sanitize_input(queryStringParameters['group'])
                if group == 'active':
                    can_receive_calls =1
                    log = 'IN'
                elif group == 'inactive':
                    can_receive_calls = 0
                    log = 'OUT'
                else:
                    raise CustomError("invalid or missing parameters", http_status_code=404, details={"message": "invalid invalid or missing parameters"})     
                active_inactive = agent.get_active_inactive_agents_in_inbound_group(can_receive_calls,log, cursor, connection)   
                
                return {
                        'statusCode': 200,
                        "headers": {
                           "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                           "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                           "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                       },                            
                        'body': json.dumps(active_inactive)
                    }                   

                                  
            if resource == "/api/agents/csd/agentphonelogsdetails"  and event['queryStringParameters'] and 'extension' in event['queryStringParameters']:
                queryStringParameters = event['queryStringParameters']
                extension = sanitize_input(queryStringParameters['extension']) 
                login_logout_details = agent.get_agent_inbound_login_logout_details(extension, cursor, connection) 
               
                return {
                        'statusCode': 200,
                        "headers": {
                           "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                           "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                           "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                       },                             
                        'body': json.dumps(login_logout_details)
                } 
           
                    
                               
            if path_parameters and all(key in path_parameters for key in ['agent_type']):
                    # Strip HTML tags and escape HTML characters in one line
                    agent_type = sanitize_input(path_parameters['agent_type'])  
                    if agent_type is None or agent_type not in ['csd', 'collection']:
                       raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "})           
                    match http_method:
                        case "GET":
                            agents = ''
                            if 'extension' not in path_parameters: # NO extension specified meaning get all agents
                                agents = agent.get_agents(agent_type, cursor, connection)
                            else:
                                extension = path_parameters['extension']
                                agents = agent.get_agent(agent_type,extension,cursor,connection)   
                          
                            return {
                                "statusCode": 200,
                                "headers": {
                                     "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                                     "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                                     "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                              },                                     
                                
                                "body": json.dumps(agents)
                            }  
                        case "POST" | "PUT":
                            body = json.loads(event['body'])
                            print(body)
                            if body is not None and all(key in body for key in ['name', 'email','extension']):
                                name =  sanitize_input(body['name']) 
                                email = sanitize_input(body['email']) 
                                extension = sanitize_input(body['extension']) 
                                create_update_agent = False
                                if http_method == 'POST':
                                    create_update_agent = agent.create_agent(name, email, extension,agent_type,cursor, connection)
                                elif http_method == "PUT":
                                   
                                    create_update_agent = agent.update_agent(name,email,extension,agent_type, cursor, connection) 
                                                                            
                                if create_update_agent:
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
                                    return {
                                        'statusCode': 201,
                                        'body': json.dumps(False)
                                    } 
                            else:
                                raise Exception({"message": "Not match Request Body"})    
                            
                        case "DELETE":
                            if 'extension' not in path_parameters:
                                raise Exception({"message": "Cannot Delete Agent Record.Agent extension is missing"})
                            extension = path_parameters['extension']
                            delete_agent = agent.delete_agent(agent_type,extension, cursor, connection)
                            
                            if delete_agent:
                                return {
                                    'statusCode': 201,
                                    "headers": {
                                        "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                                        "Access-Control-Allow-Methods": "POST,GET,OPTIONS,DELETE,PUT",
                                        "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                                    },                                         
                                    'body': json.dumps(True)
                                }    
                                
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
