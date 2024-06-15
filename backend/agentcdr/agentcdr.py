import json
import config.database as database
from datetime import datetime

db = database.connectDB()
connection = db['connection']
cursor = db['cursor']

def get_tags(tagtype):
    
    query = "SELECT * FROM tag WHERE tagtype=%s"
    
    cursor.execute(query, (tagtype,))
    
    tags = cursor.fetchall()
    
    return tags       

def sec_to_hr(seconds):
      hours = int(seconds // 3600)
      minutes = int((seconds // 60) % 60) 
      seconds = int(seconds % 60) 
      return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
 
def check_customer(caller):
    query = """ SELECT * FROM customer_info WHERE check_customer=%s"""
    
    cursor.execute(query, (caller,))
    
    customer = cursor.fetchall()
    
    customer_info = {}
    if len(customer) != 0:
        customer['isRegistered'] = True
        return customer
    else:
        return {'cid': "", "customer_number": caller, 'customer_name': "", 'updated_by': "", 'isRegistered': False }
    
def get_total_agent_cdr(startdate, enddate,tagname, extension, duration, direction,calltype ):
    if duration != "":
        duration = int(duration)
        
    if tagname =='all':
        
        match calltype:
            case "csdinbound":  
                query =  """SELECT * FROM csd_inbound_cdr WHERE getDate BETWEEN %s AND %s 
                            AND CallStatus='ANSWER' AND WhoAnsweredCall=%s 
                            ORDER BY StartTimeStamp DESC"""
                cursor.execute(query, (startdate, enddate, extension,))
            case "csdoutbound":
                
                query = ""
                if direction == "UP":
                  
                    # query = """SELECT * FROM csd_outbound_cdr WHERE getDate BETWEEN %s AND %s
                    #            AND CallStatus='ANSWER' AND Caller=%s AND CAST(Duration AS SIGNED)>=%s 
                    #            ORDER BY StartTimeStamp DESC"""
                    query =  """SELECT * FROM csd_outbound_cdr WHERE getDate BETWEEN %s AND %s AND CallStatus='ANSWER'  AND Caller = %s AND CAST(Duration AS SIGNED) >= %s ORDER BY StartTimeStamp DESC"""
                else:
                   
                    query = """SELECT * FROM csd_outbound_cdr WHERE getDate BETWEEN %s AND %s
                               AND CallStatus='ANSWER'  AND Caller=%s AND CAST(Duration AS SIGNED)<=%s
                               ORDER BY StartTimeStamp DESC""" 
                cursor.execute(query,(startdate,enddate,extension,duration,))               
            case "collection":
                query = ""
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
 
def get_call_summary(startdate, enddate, tagname, duration, direction, calltype, detailstype):
    query = ""
    if calltype == 'collection':
        query = "SELECT * FROM collection_agents"
    else:
        query =  "SELECT * FROM csd_agents"
           
    cursor.execute(query)
    agents = cursor.fetchall()

    cdr_call_summary = []
    tags = get_tags(calltype.upper())
    if len(agents) != 0 and agents:
        for agent in agents:
            # get agent total cdrs for given date range
            agent_cdrs = get_total_agent_cdr(startdate, enddate, tagname, agent['extension'], duration, direction, calltype)
            total_duration = 0
            total_counts = len(agent_cdrs)
            total = 0
            getdate = ""
            agent_name = ""

            for agent_cdr in agent_cdrs:
                starttime = agent_cdr['StartTimeStamp'].split("-")
                endtime = agent_cdr['EndTimeStamp'].split("-")

                # parse the date and time components
                end_datetime = datetime.strptime(endtime[0] + endtime[1], '%Y%m%d%H%M%S')
                start_datetime = datetime.strptime(starttime[0] + starttime[1], '%Y%m%d%H%M%S')

                total = total + (end_datetime - start_datetime).total_seconds()

                getdate = f"({startdate})-({enddate})"

                if datetime.strptime(startdate, '%Y-%m-%d') == datetime.strptime(enddate, '%Y-%m-%d'):
                    getdate = startdate
                
                if calltype == "collection":
                    agent_name = agent['name']
                else:
                    agent_name = agent['username']    
            total_duration = sec_to_hr(total)
            agent_summary = {
                "extension": agent['extension'],
                "name": agent_name,
                "total_counts": total_counts,
                "total_duration": total_duration,
                "getdate": getdate,
                "link_details": f"calldetails/{detailstype}?extension={agent['extension']}&name={agent_name}&startdate={startdate}&enddate={enddate}&tagname={tagname}"
            }

            cdr_call_summary.append(agent_summary)
        data = []
        data.append(cdr_call_summary)
        data.append(tags)
        return data

def get_call_agent_details(extension, username, startdate, enddate, tagname, duration, direction, calltype)  :
    
    tags = get_tags(calltype.upper())
    
    agent_cdrs = get_total_agent_cdr(startdate, enddate,tagname, extension, duration, direction,calltype )
    # agent_cdrs = get_total_agent_inbound_cdr('2024-05-01','2024-05-30','all','2033')
    print(agent_cdrs)
    print(len(agent_cdrs))
    if len(agent_cdrs) !=0 and agent_cdrs:
        
        agent = []
        total = 0
        for agent_cdrs in agent_cdr:
            
            customer = check_customer(agent_cdr['Caller'])
            
            starttime = agent_cdr['StartTimeStamp'].split("-")
            endtime = agent_cdr['EndTimeStamp'].split("-")
            #parse the date and time components
                
            end_datetime = datetime.strptime(endtime[0] + endtime[1], '%Y%m%d%H%M%S')
            start_datetime = datetime.strptime(starttime[0] + starttime[1],  '%Y%m%d%H%M%S')
                
            total = total + (end_datetime - start_datetime).total_seconds()
            
            duration = sec_to_hr(total)
            base_url = "http://211.0.128.110/callrecording/incoming/"
            date_folder = agent_cdr['getDate'].replace('-','')
            filename = f"{agent_cdr['Caller']-agent_cdr['CalledNumber']-agent_cdr['StartTimeStamp']}.mp3"
            full_url = f"{base_url}{date_folder}/{filename}"
            
            daterange = f"({startdate})-({enddate})"
                
                    
            if datetime.strptime(startdate, '%Y-%m-%d') == datetime.strptime(enddate, '%Y-%m-%d'):
                daterange  = startdate 

            agent_cdr['name'] = username
            agent_cdr['starttime'] = datetime.strptime(starttime[1], "%H%M%S").strftime("%I:%M:%S %p")
            agent_cdr['endtime'] =  datetime.strptime(endtime[1], "%H%M%S").strftime("%I:%M:%S %p")
            agent_cdr['callDuration'] = duration
            agent_cdr['starttimestamp'] = agent_cdr.pop('StartTimeStamp') # change the key my dictionary from StartTimeStamp to starttimestamp
            agent_cdr['isregistered'] = customer['isRegistered']
            agent_cdr['customer_name'] = customer['customer_name']
            agent_cdr['customer_number'] = customer['customer_number']
            agent_cdr['updated_by'] = customer['updated_by']
            agent_cdr['daterange'] = daterange
            
            agent.append(agent_cdr)
            
        data = []
        data.append(agent)
        data.append(tags) 
        return data
    else:
        return {"message": "No Records Found"}