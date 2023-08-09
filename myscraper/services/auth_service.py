import jwt
import os
from dotenv import load_dotenv
import time

load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))

class AuthService:
    def getJWT(username: str):
        payload = {
            "username": username,
            "expires": time.time() + JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return {"token": access_token, "type": "bearer"}

    def decodeJWT(token: str):
        try:
            decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            if decoded_token["expires"] >= time.time():
                return decoded_token['username']
            raise Exception('Expired token')
        except:
            raise Exception('Invalid token')