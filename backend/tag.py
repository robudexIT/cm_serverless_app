import json
import utils.auth as auth
import cdr.tag as tag
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
       
       accpeted_http_methods = ['GET', 'POST','DELETE']
       http_method = event['httpMethod']
       headers = event.get('headers', {})
       path_parameters = event['pathParameters']
    #    body = json.loads(event['body'])
       
       if http_method not in accpeted_http_methods or http_method is None:
           raise Exception({"message:":"HTTP METHOD IS NOT ACCEPTED"})

       match http_method:
           case "GET":
            
                 alltags = tag.select_all_tags(cursor)
                 return {
                     'statusCode': 200,
                     'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS,PUT,DELETE',
                        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                     },                     
                     'body': json.dumps(alltags)
                 }
 
                      
           case "POST": 
              tagtype = path_parameters['tagtype']
       
              if tagtype is None or tagtype not in ['collection', 'csdinbound', 'csdoutbound']:
                 raise Exception({"message": "PATH PARAMETERS ARE Invalid"})
              
              body = json.loads(event['body'])
              print(body)
              if body is not None and all(key in body for key in ['tagname', 'createdby','createddate']):
                
                   tagname = body['tagname']
                   createdby = body['createdby']
                   createddate = body['createddate']
                  
                   create_tag = False
                   create_tag = tag.create_tag(tagtype.upper(),tagname.upper(),createdby,createddate,cursor, connection) 
                   if create_tag:
                       return {
                           'statusCode': 201,
                     'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS,PUT,DELETE',
                        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                     },                           
                           'body': json.dumps(True)
                       }
                   else:
                        raise Exception({"message":"Cannot Created Tag"})    
              else:
                   raise Exception({"message": "Not match Request Body"})    
               
           case "DELETE":
                body = json.loads(event['body'])
                if body is not None and 'tagId' in body:
                    tagid = body['tagId']
                    delete_tag = tag.delete_tag(tagid,cursor,connection)
                    if delete_tag:
                     return {
                      'statusCode': 201,
                     'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS,PUT,DELETE',
                        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                     },                      
                      'body': json.dumps(True)
                     } 
                else:
                   raise Exception({"message": "no tagid in the body of the request.."})                      
        
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
    finally:
        if db:
          db.close()   