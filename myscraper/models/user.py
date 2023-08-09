from pydantic import BaseModel
    
class User(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    username: str
    hashed_password: str