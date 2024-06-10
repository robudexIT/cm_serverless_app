from jose import jwt, JWTError 
import os
from dotenv import load_dotenv
import config.database as database
from datetime import datetime, timedelta

#Load environment variable from .env file
load_dotenv()

# import requests

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM =  os.environ['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
db = database.connectDB()
connection = db['connection']
cursor = db['cursor']


def create_access_token(data : dict):
    
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({'exp': expire})
    
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encode_jwt
    

def verify_access_token(headers):
    try:
        authorization_header = headers.get('Authorization', '')
        
        if authorization_header.startswith('Bearer '):
            access_token =  authorization_header.split('Bearer ')[1]
            
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            
            data = payload.get("data")
            
            if data['extension'] is None:
                return False
            
            return True    
        else:
            return False
        
    except JWTError :
        raise Exception("Could not validate credentials")