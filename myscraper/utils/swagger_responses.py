from ..models.message import Message
from ..models.user import UserSignupResponse, UserLoginResponse

message_post_responses = {
    201: {"description": "Created", "model": Message},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "Message already exists"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
}

user_signup_responses = {
    201: {"description": "Created", "model": UserSignupResponse},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "User already exists"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
}

user_login_responses = {
    201: {"description": "Created", "model": UserLoginResponse},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "User not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
}

get_responses = {
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
}