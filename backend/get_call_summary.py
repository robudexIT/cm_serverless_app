import json
from agentcdr.agentcdr import get_call_summary
import utils.auth as auth
from datetime import datetime

startdate = ''
enddate = ''
tagname = ''

agents_cdrs = ''

def lambda_handler(event, context):
   try:
        headers = event.get('headers', {})
        verify = auth.verify_access_token(headers) 
        
        if verify:
        
            queryStringParameters = event['queryStringParameters']
            path_parameters = event['pathParameters']
            callsummaries =  path_parameters.get('callsummaries')
            print()
            #callsummaries expect this one of this values csdinbound, csdoutbound, collection
            match callsummaries:
               case "csdinbound":
                  keys  = ['startdate', 'enddate', 'tagname']
                 
                  if all(key in queryStringParameters for key in keys):  #check if startdate, enddate and tagname is queryStringParameters  return true if all keys are there
                     startdate =  queryStringParameters['startdate']
                     enddate = queryStringParameters['enddate']
                     tagname = queryStringParameters['tagname']
                  else:
                     startdate = datetime.now().strftime('%Y-%m-%d')
                     enddate = datetime.now().strftime('%Y-%m-%d')
                     tagname = "all" 
                  
                  agents_cdrs = get_call_summary(startdate, enddate, tagname, "", "", callsummaries, f"{callsummaries}details")  
                                     
               case "csdoutbound" | "collection":
                  print('it cam here')
                  keys = ['startdate', 'enddate', 'tagname', 'duration', 'direction']
                  if all(key in queryStringParameters for key in keys):
                     startdate =  queryStringParameters['startdate']
                     enddate = queryStringParameters['enddate']
                     tagname = queryStringParameters['tagname']
                     duration = queryStringParameters['duration']
                     direction = queryStringParameters['direction']                     
                  else:
                     startdate = datetime.now().strftime('%Y-%m-%d')
                     enddate = datetime.now().strftime('%Y-%m-%d')
                     tagname = "all"  
                     duration = "0"
                     direction = "UP"                    
                  agents_cdrs = get_call_summary(startdate, enddate, tagname, duration, direction, callsummaries, f"{callsummaries}details")
            
           
         
            return {
                "statusCode": 200,
                 "body": json.dumps(agents_cdrs)
                  
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
