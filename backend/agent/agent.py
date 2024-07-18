import json
from cdr.agentcdr import sec_to_hr
from datetime import datetime



def get_agents(agenttype, cursor, connection):

    query = ""
    match agenttype:
        case "csd":
            query = "SELECT * FROM csd_agents"
        case "collection":
            query = "SELECT * FROM collection_agents"
    try:
        cursor.execute(query)
        agents = cursor.fetchall()
        return agents 
    except Exception as e:
        raise Exception({"message": e})   
    
   
            
def get_agent(agenttype, extension, cursor, connection):
   
    query = ""
    match agenttype:
        case "csd":
            query = "SELECT * FROM csd_agents WHERE extension=%s"
        case "collection":
            query = "SELECT * FROM collection_agents WHERE extension=%s"
    try:
        cursor.execute(query,(extension,))
        agents = cursor.fetchone()
        return agents 
    except Exception:
        raise Exception({"message": "Cannot Get agent", "extension": extension})   
     
                

def create_agent(name, email, extension,agenttype,cursor,connection):
    # db = database.connectDB()
    # connection = db['connection']
    # cursor = db['cursor']    
    check_agent = get_agent(agenttype,extension, cursor, connection)
    if check_agent:
        raise Exception({"message": f"extension {extension} is already been used."})
    query= ""
    match agenttype:
        
        case "csd":
            query = """INSERT INTO csd_agents SET extension=%s, name=%s, email=%s, callerid='',serverip='', serverstatus='', receive_calls=0 """
            
        case "collection":
            query = """INSERT INTO collection_agents SET extension=%s, name=%s, email=%s"""
    try:
        cursor.execute(query, (extension, name, email)) 
        if cursor.rowcount >0:
            agent_calltype = get_agent_calltype(extension,agenttype,"INSERT",cursor,connection)
            if agent_calltype :
                 print("New Agent successfully added..")
                 connection.commit()
            else:
                assign_agent_calltype =  set_agent_calltype(extension,agenttype, cursor, connection)
                if assign_agent_calltype:
                   print("New Agent successfully added..")   
                   connection.commit()  
            return True 
        else:
            print("No Agent added..")
            return False
    except Exception as e: 
        raise Exception({"message": f"Cannot create agent... {e}"})
        

def update_agent(name, email, extension, agenttype,cursor, connection):
  
    check_agent = get_agent(agenttype,extension,cursor,connection)
    print(check_agent)
    if check_agent is None:
        raise Exception({"message": f"Cannot find Agent, Update failed"})
    query = ""
    match agenttype:
        case "csd":
            query = """ UPDATE csd_agents SET name = %s, email= %s WHERE extension = %s"""
        case "collection":
            query = """UPDATE collection_agents SET name = %s, email= %s WHERE extension = %s"""
    try:
        cursor.execute(query,(name,email,extension,))
        if cursor.rowcount > 0:
            
            # Update Agent calltype As well if neccesary..
            if get_agent_calltype(extension,agenttype, "UPDATE",cursor,connection):
                print("Agent Record updated successfully!")
                connection.commit()
                return True
            else:
                if update_agent_calltype(extension,agenttype,cursor,connection):
                    print('Agent calltype is updated')
                    print("Agent Record updated successfully!") 
                    return True
                    connection.commit() 
                else:
                    print('Agent calltype update failed')
                    print('Agent Record update failed')
                    return False
        else:
            print("Updated Agent Record was failed to update")
            return False
    except Exception as e:
        raise Exception({"message": "Cannot Update agent", "extension": extension})
        

def delete_agent(agenttype, extension,cursor, connection):

    check_agent = get_agent(agenttype,extension, cursor, connection)
    if check_agent is None:
        raise Exception({"message": f"Cannot find Agent, Delete failed"})    
    query = ""
    match agenttype:
        case "csd":
            query = "DELETE FROM csd_agents WHERE extension=%s"
        case "collection":
            query = "DELETE FROM collection_agents WHERE extension=%s"
    
    try:
        cursor.execute(query, (extension,))
        
        if cursor.rowcount > 0:
            print("Agent Record delete successfully")
            if delete_agent_calltype(extension,cursor,connection):
                connection.commit()
                return True 
        else:
            print("Cannot Delete Agent Record")
            return False 
    except Exception as e:
        raise Exception({"message": f"Cannot Delete agent extension: {extension} ... {e}"})   

def get_login_logout_duration(log, extension, cursor,connection):
    query = """ SELECT * FROM logs WHERE log=%s AND extension=%s ORDER by timestamp DESC LIMIT 1"""  
    cursor.execute(query,(log, extension,))
    
    log = cursor.fetchone()
    
    if log is None:
        return 0;   
   
    # Current date and time
    current_date = datetime.now()
    
    #log['timestamp'] is already datetime object is we can subtract it direct to current date an get the total in seconds
    duration = (current_date - log['timestamp']).total_seconds()
    
    duration = sec_to_hr(duration)
    
    return duration
    

def get_active_inactive_agents_in_inbound_group(can_receive_calls,log,cursor, connection):
    try:
        query = """ SELECT * FROM csd_agents WHERE receive_calls=%s """
        print(can_receive_calls)
        print(log)
       
        cursor.execute(query, (can_receive_calls,))
        agents = cursor.fetchall()
        active_inactive = []
        print(len(agents))
        if agents and len(agents) > 0:
           for agent in agents:
               agent['loginlogout'] = f"agents/csd/agentphonelogsdetails?extension={agent['extension']}"
               if log == 'IN' :
                 agent['loginduration'] = get_login_logout_duration(log, agent['extension'],cursor, connection)
               elif log == 'OUT':
                  agent['logoutduration'] = get_login_logout_duration(log, agent['extension'], cursor, connection)    
               active_inactive.append(agent) 
               
           return active_inactive
        else:
           return []     
        
    except Exception as e:
        raise Exception({"message": f"Cannot get active or inactive agents.... {e}"})
    
def get_agent_inbound_login_logout_details(extension, cursor,connection):
    try:
        query = """SELECT * FROM logs WHERE extension=%s ORDER BY timestamp DESC"""
        cursor.execute(query,(extension,))
    
        logs = cursor.fetchall()
        agent_logs = []
        if logs and len(logs) > 0: 
            for log in logs:
                agent_logs.append({
                    'log': log['log'],
                    'date': log['logdate'],
                    'time': log['logtime']
                })
            return agent_logs  
        else:
            return []
    except Exception:
        raise Exception({"message": "Cannot Get Agent Log Details"})

def set_agent_calltype(extension, agenttype,cursor,connection):
     try:
        query  = """INSERT INTO calltype SET extension= %s, calltype=%s"""
        cursor.execute(query,(extension,agenttype,))
        connection.commit()
        if cursor.rowcount > 0:
            return True
        else: 
            return False
     except Exception:
         raise Exception({"message": "Cannot INSERT into calltype"})

def get_agent_calltype(extension,agenttype,querytype,cursor, connection):
    try:
        if querytype == "INSERT":
            query = """SELECT * FROM calltype WHERE extension=%s"""
            cursor.execute(query, (extension,)) 
        elif querytype == "UPDATE":
            query = """SELECT * FROM calltype WHERE extension=%s AND calltype=%s"""
            cursor.execute(query, (extension,agenttype,)) 
            
        agent_calltype = cursor.fetchone()
        
        if agent_calltype :
            return agent_calltype 
        else:
            return False
    except Exception as e:
        raise Exception({"message": f"Error in get calltype info extention {extension} .. {e}"}) 

def update_agent_calltype(extension, agenttype,cursor, connection):
    try:
        query = """UPDATE calltype SET calltype=%s WHERE extension=%s"""
        cursor.execute(query, (agenttype, extension,))
        connection.commit()
        return True
    except Exception:
        raise Exception({"message": f"Cannot update the calltype of extension {extension}"})  
    
def delete_agent_calltype(extension, cursor, connection):
    try:
        query = """DELETE FROM calltype WHERE extension=%s"""
        cursor.execute(query,(extension,))
        connection.commit()
        if cursor.rowcount > 0:
            return True 
        else:
            return False
    except Exception as e:
        raise Exception ({"message": f"Cannot Delete Agent Calltype...{e}"})
        
                               