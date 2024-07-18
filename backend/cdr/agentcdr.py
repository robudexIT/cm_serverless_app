import json
from datetime import datetime
from utils.custom_exception import CustomError 


def get_the_time(td):
    try:
        # Try to parse the datetime string
        td  = datetime.strptime(td,"%Y%m%d-%H%M%S" )
        # Format the time to "HH:MM:SS AM/PM"
        return td.strftime("%I:%M:%S %p")

    except ValueError:
        return ""  

def get_agent_info(extension,agenttype, cursor):
    query = ""
    match agenttype:
        case "csd":
            query = "SELECT * FROM csd_agents WHERE extension=%s"
        case "collection":
            query = "SELECT * FROM collection_agents WHERE extension=%s"
    
    cursor.execute(query, (extension,))        
    agent = cursor.fetchone()
    
    return agent 

def get_tags(tagtype,cursor):
    try:
        query = "SELECT * FROM tag WHERE tagtype=%s"
        
        cursor.execute(query, (tagtype,))
        
        tags = cursor.fetchall()
        
        if tags and len(tags) > 0:
            tagname_list = []
            for tag in tags:
                tagname_list.append(tag['tagname'])
            return tagname_list
        else:
            return []
    except Exception as e:
        raise Exception({"message": f"Cannot get tags.. {e}"})      

def sec_to_hr(seconds):
      hours = int(seconds // 3600)
      minutes = int((seconds // 60) % 60) 
      seconds = int(seconds % 60) 
      return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
 
def check_customer(caller, cursor):
    try:
            
        query = """ SELECT * FROM customer_info WHERE customer_number=%s"""
        
        cursor.execute(query, (caller,))
        
        customer = cursor.fetchone()
        
    
        if customer is not None:
            customer['isRegistered'] = True
            return customer
        else:
            return {'cid': "", "customer_number": caller, 'customer_name': "", 'updated_by': "", 'isRegistered': False }
    
    except Exception as e:
        raise Exception({"message": f"Error in check_customer... {e}"})    
    
def transform_cdr(cdr,calltype,cursor):
    try:
        starttime = cdr['StartTimeStamp'].split("-")
        endtime = cdr['EndTimeStamp'].split("-")
        
        #parse the date and time components
        end_datetime = datetime.strptime(endtime[0] + endtime[1], '%Y%m%d%H%M%S')
        start_datetime = datetime.strptime(starttime[0] + starttime[1],  '%Y%m%d%H%M%S')
        total = 0 
            
        if 'Duration' in cdr:  
            total = total + int(cdr['Duration'])
        else: 
                
            total = total + (end_datetime - start_datetime).total_seconds()
                
                
        call_duration = sec_to_hr(total)
        
        filename = f"{cdr['Caller']}-{cdr['CalledNumber']}-{cdr['StartTimeStamp']}.mp3"
    
        if calltype == 'csdinbound' or calltype == 'csdinbounddetails':
                
                base_url = "http://211.0.128.110/callrecording/incoming/"
                cdr['extension']  = cdr['WhoAnsweredCall']
        else:
            base_url = "http://211.0.128.110/callrecording/outgoing/"
            cdr['extension'] = cdr['Caller']  # change the key my dictionary from WhoAnswerCall to extension     
                
        
        date_folder = cdr['getDate'].replace('-','')
    
        full_url = f"{base_url}{date_folder}/{filename}"
        
                

        cdr['starttime'] = datetime.strptime(starttime[1], "%H%M%S").strftime("%I:%M:%S %p")
        cdr['endtime'] =  datetime.strptime(endtime[1], "%H%M%S").strftime("%I:%M:%S %p")
        cdr['callDuration'] = call_duration
        cdr['callrecording'] = full_url
        cdr['starttimestamp'] = cdr.pop('StartTimeStamp') # change the key my dictionary from StartTimeStamp to starttimestamp
        
        return cdr
    except Exception as e:
        raise Exception ({"message": f"Cannot Transform CDR... {e}"})
             
def get_total_agent_cdr(startdate, enddate, startdate_and_time, enddate_and_time, tagname, extension, duration, direction,calltype,formetrics,cursor):
    try:
        query = ""
        if duration != "":
            duration = int(duration)
            
        if tagname =='all':
            
            match calltype:
                case "csdinbound": 
                    if formetrics:

                        query =  """ SELECT * FROM csd_inbound_cdr WHERE StartTimeStamp BETWEEN %s AND %s 
                                    AND  CallStatus='ANSWER' AND  WhoAnsweredCall=%s 
                                    ORDER BY StartTimeStamp DESC
                                """
                        cursor.execute(query, (startdate_and_time, enddate_and_time, extension,))             
                    else:                    
                        query =  """SELECT * FROM csd_inbound_cdr WHERE getDate BETWEEN %s AND %s 
                                AND CallStatus='ANSWER' AND WhoAnsweredCall=%s 
                                ORDER BY StartTimeStamp DESC"""
                        cursor.execute(query, (startdate, enddate, extension,))
                case "csdoutbound":
                            
                    if formetrics:

                        query =  """ SELECT * FROM csd_outbound_cdr WHERE StartTimeStamp BETWEEN %s AND %s 
                                    AND  CallStatus='ANSWER'  AND Caller=%s
                                    ORDER BY StartTimeStamp DESC
                                """
                        cursor.execute(query, (startdate_and_time, enddate_and_time, extension,))                      
                    else:
                        
                        if direction == "UP":
                            print('It came here')
                            # query = """SELECT * FROM csd_outbound_cdr WHERE getDate BETWEEN %s AND %s
                            #            AND CallStatus='ANSWER' AND Caller=%s AND CAST(Duration AS SIGNED)>=%s 
                            #            ORDER BY StartTimeStamp DESC"""
                            query =  """SELECT * FROM csd_outbound_cdr WHERE getDate BETWEEN %s AND %s AND CallStatus='ANSWER'  AND Caller = %s AND CAST(Duration AS SIGNED) >= %s ORDER BY StartTimeStamp DESC"""
                        else:
                            print('It came here instead')
                            query = """SELECT * FROM csd_outbound_cdr WHERE getDate BETWEEN %s AND %s
                                    AND CallStatus='ANSWER'  AND Caller=%s AND CAST(Duration AS SIGNED)<=%s
                                    ORDER BY StartTimeStamp DESC""" 
                        cursor.execute(query,(startdate,enddate,extension,duration,))               
                case "collection":
                    print('it came here is collection')
                    if formetrics:

                        query =  """ SELECT * FROM  collection_outbound_cdr WHERE StartTimeStamp BETWEEN %s AND %s 
                                    AND  CallStatus='ANSWER'  AND Caller=%s
                                    ORDER BY StartTimeStamp DESC
                                """
                        cursor.execute(query, (startdate_and_time, enddate_and_time, extension,))       
                    else:
                        if direction == "UP":
                            query = """SELECT * FROM  collection_outbound_cdr WHERE getDate BETWEEN %s AND %s
                                    AND CallStatus='ANSWER'  AND Caller=%s AND CAST(Duration AS SIGNED)>=%s  
                                    ORDER BY StartTimeStamp DESC""" 
                        else:
                            query = """SELECT * FROM  collection_outbound_cdr WHERE getDate BETWEEN %s AND %s
                                    AND CallStatus='ANSWER'  AND Caller=%s AND CAST(Duration AS SIGNED)<=%s  
                                    ORDER BY StartTimeStamp DESC""" 
                        cursor.execute(query,(startdate,enddate,extension,duration,))        
                            
                
        else:
            match calltype:
                case "csdinbound":
                    
                    query = """SELECT * FROM csd_inbound_cdr WHERE getDate BETWEEN %s AND %s AND 
                                CallStatus='ANSWER'  AND WhoAnsweredCall=%s  AND tag=%s ORDER BY StartTimeStamp DESC"""
                    cursor.execute(query, (startdate, enddate,extension,tagname,))    
                            
                case "csdoutbound":
                    query = ""
                    if direction == "UP":
                        query = """SELECT * FROM csd_outbound_cdr WHERE getDate BETWEEN %s AND %s
                                AND CallStatus='ANSWER'  AND Caller=%s AND tag=%s AND CAST(Duration AS SIGNED)>=%s 
                                ORDER BY StartTimeStamp DESC"""
                    else:
                        query = """SELECT * FROM csd_outbound_cdr WHERE getDate BETWEEN %s AND %s
                                AND CallStatus='ANSWER'  AND Caller=%s AND tag=%s AND CAST(Duration AS SIGNED)<=%s
                                ORDER BY StartTimeStamp DESC""" 
                    cursor.execute(query,(startdate,enddate,extension,tagname,duration,))                               
                case "collection":
                    query = ""
                    if direction == "UP":
                        query = """SELECT * FROM  collection_outbound_cdr WHERE getDate BETWEEN %s AND %s
                                AND CallStatus='ANSWER'  AND Caller =%s AND tag=%s AND CAST(Duration AS SIGNED)>=%s  
                                ORDER BY StartTimeStamp DESC""" 
                    else:
                        query = """SELECT * FROM  collection_outbound_cdr WHERE getDate BETWEEN %s AND %s
                                AND CallStatus='ANSWER'  AND Caller =%s AND tag=%s AND CAST(Duration AS SIGNED)<=%s  
                                ORDER BY StartTimeStamp DESC""" 
                    cursor.execute(query,(startdate,enddate,extension,tagname,duration,))                   
        
        
        agent_cdrs = cursor.fetchall()
        return agent_cdrs    
    except Exception as e:
        raise Exception({"message": f"error in get_total_agent_cdr {e}"}) 
    
def get_call_summary(startdate, enddate, startdate_and_time, enddate_and_time, tagname, duration, direction, calltype, detailstype, formetrics,cursor):
    
    try:

        query = ""
        print(calltype)
        if calltype == 'collection':
            query = "SELECT * FROM collection_agents"
        elif calltype == 'csdinbound' or calltype == 'csdoutbound':
            query =  "SELECT * FROM csd_agents"
          
        elif calltype == 'sales':
            query = "SELECT * FROM sales_agents"
    
        # if calltype is equal missedcalls
        elif calltype == 'missedcalls':
            getdate = ""
            if datetime.strptime(startdate, '%Y-%m-%d') == datetime.strptime(enddate, '%Y-%m-%d'):
                getdate = startdate
            else:
                getdate = f"({startdate})-({enddate})"  
            query = """ SELECT * FROM csd_inbound_cdr WHERE CallStatus !='ANSWER' AND getDate BETWEEN %s AND %s ORDER BY getDate DESC """
            cursor.execute(query,(startdate,enddate,))
            missedcalls = cursor.fetchall()
            
            
            if missedcalls and len(missedcalls) > 0 :
                return [
                    {
                        "total_missed_calls": len(missedcalls),
                        "getdate": getdate,
                        "link_details":  f"calldetails/{detailstype}?startdate={startdate}&enddate={enddate}"
                    }
                ]
            else:
                return [] 
        else:
            raise CustomError("Calltype is invalid...", http_status_code=403, details={"message": "Calltype is invalid..."})     
            
        cursor.execute(query)
        agents = cursor.fetchall()
       
        cdr_call_summary = []
        data = [] 
        tags = get_tags(calltype.upper(),cursor)
        grand_total_duration_sec = 0
        grand_total_counts = 0    
        if len(agents) != 0 and agents:
            for agent in agents:
                # get agent total cdrs for given date range
                agent_cdrs = get_total_agent_cdr(startdate, enddate, startdate_and_time, enddate_and_time, tagname, agent['extension'], duration, direction, calltype,formetrics,cursor)

                total_duration = 0
                total_counts = len(agent_cdrs)
               
                total = 0
                getdate = ""
                agent_name = ""
                
                #this variable is for metrics

                
                
                for agent_cdr in agent_cdrs:
                    if 'Duration' in agent_cdr:
                        total = total + int(agent_cdr['Duration'])
                    else:
                        starttime = agent_cdr['StartTimeStamp'].split("-")
                        endtime = agent_cdr['EndTimeStamp'].split("-")

                        # parse the date and time components
                        end_datetime = datetime.strptime(endtime[0] + endtime[1], '%Y%m%d%H%M%S')
                        start_datetime = datetime.strptime(starttime[0] + starttime[1], '%Y%m%d%H%M%S')
                        
                        total = total + (end_datetime - start_datetime).total_seconds()      
                        #add this additional data if formetris is true 
                        

                if formetrics :
                    grand_total_duration_sec = grand_total_duration_sec + total 
                    grand_total_counts =   grand_total_counts + total_counts
                    agent['total_sec'] = total     
                    
                else:
                    agent['link_details']  = f"calldetails/{detailstype}?extension={agent['extension']}&name={agent['name']}&startdate={startdate}&enddate={enddate}&tagname={tagname}&duration={duration}&direction={direction}"  
                    getdate = ""
                    if datetime.strptime(startdate, '%Y-%m-%d') == datetime.strptime(enddate, '%Y-%m-%d'):
                        getdate = startdate
                    else:
                       getdate = f"({startdate})-({enddate})"  
                       agent['getdate'] = getdate
                    
                    
                total_duration = sec_to_hr(total)
                # agent_summary = {
                #     "extension": agent['extension'],
                #     "name": agent['name'],
                #     "total_counts": total_counts,
                #     "total_duration": total_duration,
                #     "getdate": getdate,
                #     "link_details": f"calldetails/{detailstype}?extension={agent['extension']}&name={agent['name']}&startdate={startdate}&enddate={enddate}&tagname={tagname}&duration={duration}&direction={direction}"
                # }
                agent['total_counts'] = total_counts
                agent['total_duration'] = total_duration

                

                cdr_call_summary.append(agent)
            
            data.append(cdr_call_summary)
         
            if formetrics: 
                grand_total_duration = sec_to_hr(grand_total_duration_sec)
                grand_total = {
                    'grand_total_duration_sec': grand_total_duration_sec,
                    'grand_total_duration': grand_total_duration,
                    'grand_total_counts': grand_total_counts,
                    'option': calltype
                }
                data.append(grand_total)
               
           
            else:
                tags = get_tags(calltype.upper(),cursor)       
                data.append(tags)
            print(type(data))
            return data
        else:
            return []
        
    except Exception as e:
        raise Exception ({"message": f"Error in fetch callsummaries... {e}"})    
  
def get_call_agent_details(extension, username, startdate, enddate, tagname, duration, direction, calltype,cursor)  :
    try:
        
        if calltype == 'missedcalls':
            query = """SELECT * FROM csd_inbound_cdr WHERE CallStatus !=%s AND getDate BETWEEN %s AND %s ORDER BY getDate DESC"""
            cursor.execute(query,('ANSWER',startdate, enddate,))
            missedcallsdetails = cursor.fetchall()
                            
            if missedcallsdetails and len(missedcallsdetails) != 0:
                data = []
                
                for missedcalls in missedcallsdetails:

                    customer = check_customer(missedcalls['Caller'],cursor)
          
                    missedcalls['starttime'] = get_the_time(missedcalls['StartTimeStamp'])
                    missedcalls['endtime'] = get_the_time(missedcalls['EndTimeStamp'])
                    missedcalls['isRegistered'] = customer['isRegistered']
                    missedcalls['customer_id'] = customer['cid']
                    missedcalls['customer_number'] = customer['customer_number']
                    missedcalls['customer_name'] = customer['customer_name']
                    missedcalls['updated_by'] = customer['updated_by']
                    
                    data.append(missedcalls)
                 
                return data
            else:
                return []
       
        tags = get_tags(calltype.upper(),cursor)
                     
        agent_cdrs = get_total_agent_cdr(startdate, enddate, "", "", tagname, extension, duration, direction,calltype,False,cursor )
        
    
    
        if len(agent_cdrs) !=0 and agent_cdrs:
            
            agent = []
            total = 0
            base_url = ""
            customer = ""
            
            for agent_cdr in agent_cdrs:
            
            
                transformed_agent_cdr = []
                if calltype == "csdinbound":
                    
                    customer = check_customer(agent_cdr['Caller'],cursor)
                else:
                    customer = check_customer(agent_cdr['CalledNumber'][3:],cursor) 
                    
                transformed_agent_cdr = transform_cdr(agent_cdr,calltype,cursor)
                
            
                daterange = f"({startdate})-({enddate})"
                    
                        
                if datetime.strptime(startdate, '%Y-%m-%d') == datetime.strptime(enddate, '%Y-%m-%d'):
                  daterange  = startdate  

                transformed_agent_cdr['name'] = username  
                transformed_agent_cdr['isregistered'] = customer['isRegistered']
                transformed_agent_cdr['customer_name'] = customer['customer_name']
                transformed_agent_cdr['customer_number'] = customer['customer_number']
                transformed_agent_cdr['customer_id'] = customer['cid']
                transformed_agent_cdr['updated_by'] = customer['updated_by']
                transformed_agent_cdr['daterange'] = daterange

            
                agent.append(transformed_agent_cdr)
                
        
            data = []
            data.append(agent)
            data.append(tags) 
            
            return data
        else:
            return []
        
    except Exception as e:
        raise Exception({"message": f"There is an error in fetching calls details..{e}"})  
                         
def get_search_number(number, search_type,cursor):
    try:
        tags = get_tags(search_type.upper(),cursor)
        query = ""
        result_array = []  
        match search_type:
            case "csdinbounddetails":
                query = """SELECT * FROM  csd_inbound_cdr WHERE Caller=%s AND CallStatus='ANSWER' ORDER BY getDate DESC"""
            case "csdoutbounddetails":
                query = """SELECT * FROM csd_outbound_cdr WHERE CalledNumber=%s ORDER BY getDate DESC """
            case "collectiondetails":
                query = """SELECT * FROM collection_outbound_cdr WHERE CalledNumber=%s ORDER BY getDate DESC """   
            case "customer" :
                query = """ SELECT * FROM customer_info WHERE customer_number=%s """   
            
                
        
        cursor.execute(query, (number,))
        
        search_result = cursor.fetchall()
        
        if len(search_result) != 0: 
            if search_type == 'customer':
                return search_result
            
            customer = ""  
            if search_type == "collectiondetails" or search_type == "csdoutbounddetails" or search_type == "sales": #strip the first digit mostly in our case we are removing the '010'
                customer = check_customer(number[3:],cursor)
            else:
                customer = check_customer(number,cursor) 
                
            for search in search_result:
            
                agent_cdr = transform_cdr(search,search_type,cursor)  
                agent_cdr['isregistered'] = customer['isRegistered']
                agent_cdr['customer_name'] = customer['customer_name']
                agent_cdr['customer_number'] = customer['customer_number']
                agent_cdr['updated_by'] = customer['updated_by']
                agent_cdr['customer_id'] = customer['cid']
            
            
            match search_type:
                case "csdinbounddetails":
                    agent = get_agent_info(search['WhoAnsweredCall'],"csd",cursor)
                    if agent and len(agent) !=0:
                        agent_cdr['whoanswered'] = agent['name']
                    else:
                        agent_cdr['whoanswered'] = 'No Agent'
                case "csdoutbounddetails":
                        agent = get_agent_info(search['Caller'],"csd",cursor)
                        if agent and len(agent) !=0:
                            agent_cdr['caller'] = agent['name'] 
                        else:
                            agent_cdr['caller']  = "SalesAgent"
                case "collectiondetails":
                        agent = get_agent_info(search['Caller'], "collection",cursor)
                        if agent and len(agent) != 0:
                            agent_cdr['caller']  = agent['name']  
                        else:
                            agent['caller'] = "SalesAgent" 
                            
            result_array.append(agent_cdr)                         

            data = []
        
            data.append(result_array)
            data.append(tags)
            return data
        else: 
            return []
    except Exception as e:
        raise Exception({"message": f"Error in searching number ... {e}"})    

def get_metrics_based_on_tag(transform_start_date_and_time, transfrom_end_date_and_time, option,cursor):
    try:
        query = ""
        cdr = []
        months_year = {}
        match option:
            case "csdinbound":
                query = """SELECT * FROM csd_inbound_cdr WHERE StartTimeStamp BETWEEN %s AND %s ORDER BY StartTimeStamp ASC """
            case "csdoutbound":
                query = """SELECT * FROM csd_outbound_cdr WHERE StartTimeStamp BETWEEN %s AND %s ORDER BY StartTimeStamp ASC """
            case "collection":
                query = """SELECT * FROM  collection_outbound_cdr WHERE StartTimeStamp BETWEEN %s AND %s ORDER BY StartTimeStamp ASC """
            case "sales": 
                query = """SELECT * FROM  sales_outbound_cdr WHERE StartTimeStamp BETWEEN %s AND %s ORDER BY StartTimeStamp ASC """
        cursor.execute(query, (transform_start_date_and_time, transfrom_end_date_and_time,)) 
        
        cdrs = cursor.fetchall()
         
        data ={}
        month_year_dict = {}
        if cdrs and len(cdrs) > 0:
            #get the months and store it in month_year_dict
            for cdr in cdrs:
                dt = datetime.strptime(cdr['getDate'], "%Y-%m-%d")
                #Get the year and month name 
                year = dt.year 
                month_name = dt.strftime("%B")
                month_year = f"{month_name}{year}"
                
                #check if month_year is not exist in months_year dict add if not exist.
                if month_year not in month_year_dict:
                    month_year_dict[month_year] = 0
            
            
            #sort cdr according to tag              
            for cdr in cdrs:
                dt = datetime.strptime(cdr['getDate'], "%Y-%m-%d")
                #Get the year and month name 
                year = dt.year 
                month_name = dt.strftime("%B")
                month_year = f"{month_name}{year}"
                tag = ''
                if cdr['tag'] == '':
                    tag = 'NO TAG'
                else:
                    tag = cdr['tag']
                
                if cdr['CallStatus'] != 'ANSWER' and option == 'csdinbound':
                    tag = 'MISSEDCALLS'
                            
            
                if tag in data:
                    print(f"{tag} is already add just add one")
                    data[tag][month_year] = data[tag][month_year] + 1
                    
                else:
                    print(f"{tag} is not yet added add it")
                    data[tag] = dict(month_year_dict) 
                    data[tag][month_year] = 1                
                        
            
         
            #get all tags according to options if the tag dont exist in the data. at it as key and the value is the month_year_dict        
            tagnames = get_tags(option.upper(),cursor) 
            
            for tagname in tagnames:
                if tagname  not in data:
                   data[tagname] = dict(month_year_dict) 
            
            data['option_metrics'] = 'tag'
            data['option'] = option 
            data['total_records'] = len(cdrs) 
            print(month_year_dict)
            return data 
      
        else:
            return []         
                
                        
    except Exception as e:
        raise Exception({"message": f"Error in Generating metrics base on tag.. {e}"})     
     
def get_single_cdr(cdrtype,extension,getdate,starttimestamp,cursor):
    try:
        
        query = ''
        if cdrtype == 'csdinbound':
            query = """SELECT * FROM  csd_inbound_cdr WHERE WhoAnsweredCall=%s AND getDate=%s AND StartTimeStamp=%s"""
        elif cdrtype == "csdoutbound":
            query = """SELECT * FROM  csd_outbound_cdr WHERE Caller=%s AND getDate=%s AND StartTimeStamp=%s """  
        elif cdrtype == 'collection':
            query = """SELECT * FROM  collection_outbound_cdr WHERE Caller=%s AND getDate=%s AND StartTimeStamp=%s """      
        
        cursor.execute(query, (extension,getdate,starttimestamp,))
        
        cdr = cursor.fetchone()
        
        if not cdr or len(cdr) == 0:
            return {}
        else:
            return cdr
        
    except Exception as e:
        raise Exception({"message:":f"Error in fetch cdr.... {e}"})    
    
    
def update_single_cdr(cdrtype, extension,getdate, starttimestamp,comment,commentby,tag,cursor,connection):
    try:
        query = ''
        if cdrtype == 'csdinbound':
            query = "UPDATE csd_inbound_cdr SET comment=%s, commentby=%s,tag=%s WHERE StartTimeStamp=%s AND getDate=%s AND WhoAnsweredCall=%s"""
        elif cdrtype == 'csdoutbound':
            query = """UPDATE csd_outbound_cdr SET comment=%s, commentby=%s, tag=%s WHERE StartTimeStamp=%s AND getDate=%s AND Caller=%s"""
        elif cdrtype == 'collection':
            query = """UPDATE csd_outbound_cdr SET comment=%s, commentby=%s, tag=%s WHERE StartTimeStamp=%s AND getDate=%s AND Caller=%s"""
        
        cursor.execute(query,(comment,commentby,tag,starttimestamp,getdate,extension,))
            
        if cursor.rowcount > 0:
            connection.commit()
            return True
        else:
            return False        
    except Exception as e:
        raise Exception({"message": f"Error in udpating cdr...{e}"})    
        
def insert_update_delete_customer(querytype, customer_id, customer_name, customer_number, updated_by,cursor,connection):
   try: 
        query = ''
        if querytype == 'insert':
            query = """INSERT INTO customer_info SET  cid = %s, customer_number = %s, customer_name = %s, updated_by = %s""" 
            print('it came to this insert block')
            cursor.execute(query, (customer_id,customer_number,customer_name,updated_by,)) 
        elif querytype == 'update':
            query = """UPDATE customer_info SET cid =%s, customer_number=%s ,customer_name=%s,  updated_by=%s  WHERE customer_number=%s """
            cursor.execute(query, (customer_id,customer_number,customer_name, updated_by, customer_number,)) 
        elif querytype == 'delete':
            query = """ DELETE FROM customer_info WHERE cid=%s AND customer_number=%s  AND customer_name=%s AND updated_by=%s"""
            cursor.execute(query, (customer_id,customer_number,customer_name,updated_by,))
        
        if cursor.rowcount > 0:
            connection.commit()
            return True
        else:
            return False   
   except Exception as e:
       raise Exception({"message": f"Error in {querytype}ing customer ... {e}"})  
   
             
      