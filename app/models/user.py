from pydantic import BaseModel
    
class User(BaseModel):
    username: str
    password: str
    
class UserSignupResponse(BaseModel):
    username: str
    hashed_password: str
    
class UserLoginResponse(BaseModel):
    token: str