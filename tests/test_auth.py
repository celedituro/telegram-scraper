import sys
import pytest
import os
import time
import jwt
from unittest.mock import patch
sys.path.append("..")
from dotenv import load_dotenv

from api.auth import Auth
from api.exceptions.auth_exceptions import ExpiredToken, InvalidToken

load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))

def test_01_generate_and_decode_jwt():
    auth = Auth()

    username = "testuser"
    token = auth.getJWT(username)

    decoded_username = auth.decodeJWT(token)
    assert decoded_username == username

def test_02_expired_token():
    auth = Auth()

    payload = {
        "username": "expireduser",
        "expires": time.time() - 3600  # Expired one hour ago
    }
    expired_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    with pytest.raises(ExpiredToken):
        auth.decodeJWT(expired_token)

def test_03_invalid_token():
    auth = Auth()

    payload = {
        "username": "testuser",
        "expires": time.time() + 3600
    }
    invalid_token = jwt.encode(payload, "wrong_secret_key", algorithm=JWT_ALGORITHM)

    with pytest.raises(InvalidToken):
        auth.decodeJWT(invalid_token)