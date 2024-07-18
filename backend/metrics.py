import json
from cdr.agentcdr import get_call_summary,  get_metrics_based_on_tag
from utils.sanitize import sanitize_input
from utils.custom_exception import CustomError 
import utils.auth as auth
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
            keys = ['group', 'start_date_and_time', 'end_date_and_time','option_metrics','duration_weight', 'callcount_weight'] 
            generate_metrics = []
            if queryStringParameters is not None and all(key in queryStringParameters for key in keys): 
               
              calltype = sanitize_input(queryStringParameters['group']) 
              start_date_and_time = sanitize_input(queryStringParameters['start_date_and_time']) 
              end_date_and_time = sanitize_input(queryStringParameters['end_date_and_time']) 
              option_metrics = sanitize_input(queryStringParameters['option_metrics']) 
              duration_weight = sanitize_input(queryStringParameters['duration_weight']) 
              callcount_weight = sanitize_input(queryStringParameters['callcount_weight'])
              transform_start_date_and_time = start_date_and_time.strip().replace(":", "").replace("-", "").replace(" ", "-")
              transfrom_end_date_and_time =  end_date_and_time.strip().replace(":", "").replace("-", "").replace(" ", "-")              
              if option_metrics == 'tag':
                generate_metrics = get_metrics_based_on_tag(transform_start_date_and_time, transfrom_end_date_and_time, calltype,cursor)                   

              else:

                  generate_metrics = get_call_summary("", "", transform_start_date_and_time , transfrom_end_date_and_time, "all", "", "", calltype, "", True,cursor)
                  generate_metrics[1]['duration_weight'] = duration_weight
                  generate_metrics[1]['callcount_weight'] = callcount_weight
                  generate_metrics[1]['datetimeRange'] = f"{start_date_and_time}  To {end_date_and_time}"
              
              # print(generate_metrics)    
              return {
                  'statusCode': 200,
                  "headers": {
                     "Access-Control-Allow-Origin": "*",  # Allow all origins for local testing; specify origins for production
                      "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                      "Access-Control-Allow-Headers": "Content-Type,Authorization,Access-Control-Allow-Origin"
                    },                       
                  'body': json.dumps(generate_metrics)
              }
            else:
               raise CustomError("There are missing query", http_status_code=404, details={"message": "There are missing query"})  
                    

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