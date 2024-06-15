import json
import utils.auth as auth
from agentcdr.agentcdr import  get_call_agent_details


extension = ''
username = ''
startdate = ''
enddate = ''
username = ''
tagname = ''
calltype = ''
agents_inbound_cdrs_details = ''
def lambda_handler(event, context):
   try:  
        headers = event.get('headers', {})
        verify = auth.verify_access_token(headers)
        
        if verify:         
                queryStringParameters = event['queryStringParameters']
                path_parameters = event['pathParameters']
                calldetails =  path_parameters.get('calldetails')
                
                match calldetails:
                    case "csdinbounddetails":
                        calltype = "csdinbound"
                       
                        keys1  = ['extension', 'name', 'startdate', 'enddate','tagname']   
                        keys2  = ['modalextension', 'modalname', 'startdate', 'enddate','tagname']
                        if all(key in queryStringParameters for key in keys1):  #check if startdate, enddate and tagname are in queryStringParameters then return true
                            extension =  queryStringParameters['extension']
                            username = queryStringParameters['name']
                            startdate =  queryStringParameters['startdate']
                            enddate = queryStringParameters['enddate']
                            tagname = queryStringParameters['tagname']
                    
                        elif all(key in queryStringParameters for key in keys2):
                            extension =  queryStringParameters['modalextension']
                            username = queryStringParameters['modalname']
                            startdate =  queryStringParameters['startdate']
                            enddate = queryStringParameters['enddate']
                            tagname = queryStringParameters['tagname']
                        agents_inbound_cdrs_details = get_call_agent_details(extension, username, startdate, enddate, tagname, "", "", calltype) 
                        
                                    
                    case "csdoutbounddetails" | "collectiondetails":
                        #remove the 'details'
                        to_remove = 'details'
                        calltype = calldetails.replace(to_remove, "")
                        keys1  = ['extension', 'name', 'startdate', 'enddate','tagname','duration', 'direction']   
                        keys2  = ['modalextension', 'modalname', 'startdate', 'enddate','tagname', 'duration','direction']                        
                        
                        if all(key in queryStringParameters for key in keys1):  #check if startdate, enddate and tagname are in queryStringParameters then return true
                            extension =  queryStringParameters['extension']
                            username = queryStringParameters['name']
                            startdate =  queryStringParameters['startdate']
                            enddate = queryStringParameters['enddate']
                            tagname = queryStringParameters['tagname']
                            duration = queryStringParameters['duration']
                            direction = queryStringParameters['direction']
                    
                        elif all(key in queryStringParameters for key in keys2):
                            extension =  queryStringParameters['modalextension']
                            username = queryStringParameters['modalname']
                            startdate =  queryStringParameters['startdate']
                            enddate = queryStringParameters['enddate']
                            tagname = queryStringParameters['tagname']
                            duration = queryStringParameters['duration']
                            direction = queryStringParameters['direction']                            
                        agents_inbound_cdrs_details = get_call_agent_details(extension, username, startdate, enddate, tagname, duration, duration, calltype) 
                        
                return {
                    "statusCode": 200,
                    "body": json.dumps(agents_inbound_cdrs_details)
                    
                }
                
    
        else:
            raise Exception({"message": "Not Authorize!!", "http_status_code": 401}) 
 
   except Exception as e:
    # #    error = json.dumps(str(e))
    # #    print(type(error))
    #    print(error)
    #    error_dict = json.loads(error)
    #    print(type(error_dict))
       return {
            "statusCode": 500, # json.loads(error)['http_status_code'],
            'body': json.dumps(f'Error: {str(e)}')
        }
    

