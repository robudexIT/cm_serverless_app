import json
import utils.auth as auth
from cdr.agentcdr import  get_call_agent_details
from utils.sanitize import sanitize_input
from config.database import Database
from utils.custom_exception import CustomError 


extension = ''
username = ''
startdate = ''
enddate = ''
username = ''
tagname = ''
calltype = ''
agents_inbound_cdrs_details = ''
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
        queryStringParameters = event['queryStringParameters']   
        if verify:         
                
                path_parameters = event['pathParameters']
                calldetails =  sanitize_input(path_parameters.get('calldetails')) 
                
                match calldetails:
                    case "csdinbounddetails":
                        
                        calltype = "csdinbound"
                       
                        keys1  = ['extension', 'name', 'startdate', 'enddate','tagname']   
                        keys2  = ['modalextension', 'modalname', 'startdate', 'enddate','tagname']
                        if queryStringParameters  is None:
                            raise CustomError("query are missing, invalid or incomplete..", http_status_code=404, details={"message": "query are missing, invalid or incomplete.."})
                                     
                        if all(key in queryStringParameters for key in keys1):  #check if startdate, enddate and tagname are in queryStringParameters then return true
                            extension = sanitize_input(queryStringParameters['extension']) 
                            username = sanitize_input(queryStringParameters['name']) 
                            startdate = sanitize_input(queryStringParameters['startdate']) 
                            enddate = sanitize_input(queryStringParameters['enddate']) 
                            tagname = sanitize_input(queryStringParameters['tagname']) 
                    
                        elif all(key in queryStringParameters for key in keys2):
                            extension = sanitize_input(queryStringParameters['modalextension'])
                            username = sanitize_input(queryStringParameters['modalname']) 
                            startdate = sanitize_input(queryStringParameters['startdate']) 
                            enddate = sanitize_input(queryStringParameters['enddate']) 
                            tagname = sanitize_input(queryStringParameters['tagname']) 
                        
                        else:
                            raise CustomError("query are missing, invalid or incomplete..", http_status_code=404, details={"message": "query are missing, invalid or incomplete.."})
                        agents_inbound_cdrs_details = get_call_agent_details(extension, username, startdate, enddate, tagname, "", "", calltype, cursor)             
                    case "csdoutbounddetails" | "collectiondetails":
                        #remove the 'details'
                        to_remove = 'details'
                        calltype = calldetails.replace(to_remove, "")
                        keys1  = ['extension', 'name', 'startdate', 'enddate','tagname','duration', 'direction']   
                        keys2  = ['modalextension', 'modalname', 'startdate', 'enddate','tagname', 'duration','direction']                        
                      
                        if queryStringParameters  is None:
                            raise CustomError("query are missing, invalid or incomplete..", http_status_code=404, details={"message": "query are missing, invalid or incomplete.."})
                       
                        if all(key in queryStringParameters for key in keys1):  #check if startdate, enddate and tagname are in queryStringParameters then return true
                           
                            extension = sanitize_input(queryStringParameters['extension']) 
                            username = sanitize_input(queryStringParameters['name']) 
                            startdate = sanitize_input( queryStringParameters['startdate'])
                            enddate = sanitize_input(queryStringParameters['enddate']) 
                            tagname = sanitize_input(queryStringParameters['tagname']) 
                            duration = sanitize_input(queryStringParameters['duration']) 
                            direction = sanitize_input(queryStringParameters['direction']) 
                    
                        elif all(key in queryStringParameters for key in keys2):
                            extension =  sanitize_input(queryStringParameters['modalextension']) 
                            username = sanitize_input(queryStringParameters['modalname']) 
                            startdate = sanitize_input(queryStringParameters['startdate'])  
                            enddate = sanitize_input(queryStringParameters['enddate']) 
                            tagname = sanitize_input(queryStringParameters['tagname']) 
                            duration = sanitize_input(queryStringParameters['duration']) 
                            direction = sanitize_input(queryStringParameters['direction']) 
                        else:
                            raise CustomError("query are missing, invalid or incomplete..", http_status_code=404, details={"message": "query are missing, invalid or incomplete.."})                               
                        agents_inbound_cdrs_details = get_call_agent_details(extension, username, startdate, enddate, tagname, duration, direction, calltype,cursor) 
                    case "salesdetails":
                        pass  
                    case "missedcallsdetails":
                          calltype = "missedcalls"
                          if queryStringParameters  is None:
                              raise CustomError("query are missing, invalid or incomplete..", http_status_code=404, details={"message": "query are missing, invalid or incomplete.."})
                          if all(key in queryStringParameters for key in ['startdate', 'enddate']):
                              startdate = sanitize_input(queryStringParameters['startdate']) 
                              enddate  = sanitize_input(queryStringParameters['enddate']) 
                              agents_inbound_cdrs_details = get_call_agent_details("", "", startdate, enddate, "", "", "", calltype,cursor)
                          else:
                             raise CustomError("query are missing, invalid or incomplete..", http_status_code=404, details={"message": "query are missing, invalid or incomplete.."})      
                    case _:
                        raise CustomError("the details parameter are invalid..", http_status_code=404, details={"message": "the details parameter are invalid.."})
                    
                return {
                    "statusCode": 200,
                     "headers": {
                           "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                           "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                           "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                    },                         
                    "body": json.dumps(agents_inbound_cdrs_details)
                    
                }
                
    
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
  