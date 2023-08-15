import jwt
import os
import time

from dotenv import load_dotenv
from loguru import logger

from ..exceptions.auth_exceptions import ExpiredToken, InvalidToken

load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))

class AuthService:
    """
    A class responsible for handling authentication using JSON Web Tokens (JWT).

    Methods:
        getJWT(username: str): Generates a JWT for the provided username.
        decodeJWT(token: str): Decodes and validates a JWT to retrieve the username.

    Notes:
        This class provides methods to generate and decode JWT tokens for user authentication.
    """
    
    def getJWT(self, username: str):
        """
        Generates a JSON Web Token (JWT) for the provided username.

        Args:
            username (str): The username of the user.

        Returns:
            str: The generated JWT token.
        """
        payload = {
            "username": username,
            "expires": time.time() + JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token

    def decodeJWT(self, token: str):
        """
        Decodes and validates a JSON Web Token (JWT) to retrieve the username.

        Args:
            token (str): The JWT token to decode and validate.

        Returns:
            str: The username retrieved from the decoded JWT.

        Raises:
            Exception: If the token is expired or invalid.

        Notes:
            This method decodes and validates the provided JWT token, retrieving the username from the payload.
        """
        try:
            decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            if decoded_token["expires"] >= time.time():
                return decoded_token['username']
            raise ExpiredToken('The token is expired')
        except ExpiredToken as e:
            logger.error(f"[AUTH]: Error when decoding JWT {e}")
            raise ExpiredToken('The token is expired')
        except Exception as e:
            logger.error(f"[AUTH]: Error when decoding JWT {e}")
            raise InvalidToken('The token is invalid')
