import json

def select_all_tags(cursor):
    try:
        cursor.execute("""SELECT * FROM tag """)
        alltags = cursor.fetchall()
        if alltags and len(alltags) > 0:
            return alltags
        else:
            return []
    except Exception as e:
        raise Exception({"message": f"Call get all tags.. {e}"})    
def select_tags(tagtype,cursor):
    try:
        query = """ SELECT * FROM tag WHERE tagtype=%s """
        cursor.execute(query, (tagtype,))
        
        tags = cursor.fetchall()
        
        if tags and len(tags) > 0:
            tagname_list
            for tag in tags:
                tagname_list.append(tag['tagname'])
                
            return tagname_list    
        else:
            return []
        
    except Exception as e:
        raise Exception({"message":f"Error in querying tags... {e}"})
def create_tag(tagtype, tagname,createdby,createddate,cursor,connection):
    try:
        #check tag
        tagId = f"{tagtype}-{tagname}"
        query = """SELECT COUNT(*) FROM tag WHERE tagId=%s"""
        cursor.execute(query,(tagId,))
        tag = cursor.fetchone()
        if tag['COUNT(*)'] != 0:
            raise Exception({"message": "Tag is already created. Cannot Duplicate Tag"})
         
        query = """ INSERT INTO tag SET  tagId=%s, tagtype = %s, tagname = %s, createdby = %s, createddate = %s"""
        
        
        cursor.execute(query,(tagId, tagtype, tagname,createdby, createddate, ))
        connection.commit()
        if cursor.rowcount > 0: 
            print(tagId)
            return True
        else:
            return False
        
    except Exception as e:
        raise Exception({"message":f"Cannot Create Tag ...{e}"})
    

def delete_tag(tagId,cursor,connection):
    try:
        #check_tag
        #check tag
        query = """SELECT COUNT(*) FROM tag WHERE tagId=%s"""
        cursor.execute(query,(tagId,))
        tag = cursor.fetchone()
        if tag['COUNT(*)'] == 0:
            raise Exception({"message": "Cannot Delete tag which doesnt exist"})
        
        query = """ DELETE FROM tag WHERE tagId=%s"""
        cursor.execute(query,(tagId,)) 
        connection.commit()
        if cursor.rowcount > 0: 
            return True 
        else:
            return False
              
    except Exception as e:
        raise Exception({"message": f"Cannot Delete Tag... {e}"})
