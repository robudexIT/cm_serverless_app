from jose import jwt, JWTError 
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from utils.custom_exception import CustomError 

#Load environment variable from .env file
load_dotenv()

# import requests

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM =  os.environ['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])



def create_access_token(data : dict):
    try:
        
        to_encode = data.copy()
        
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({'exp': expire})
        
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encode_jwt
    except Exception :
        raise Exception({"message":"Cannot Create Token"})
    

def verify_access_token(headers):
    try:
        authorization_header = headers.get('Authorization', '')
        
        if authorization_header.startswith('Bearer '):
            access_token =  authorization_header.split('Bearer ')[1]
            
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            
            data = payload.get("data")
            
            if data['extension'] is None:
                return False 
            
            # Another Check to be implemented here!! check the extension if present in the database..
            
            
            return True    
        else:
            return False
        
    except JWTError :
        raise CustomError("Could Not Validate Token is Invalid", http_status_code=403, details={"message": "Could Not Validate Token is Invalid"})
    
        