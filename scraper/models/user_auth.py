from loguru import logger
import sys
sys.path.append("..")

from api.models.data_models import User
from scraper.utils.constants import API_URL

class UserAuth:
    """
    A class for handling user authentication operations such as signing up and logging in.
    """
    
    async def signup_user(self, client, user: User):
        """
        Sign up a new user by sending a POST request to the user registration endpoint.

        Args:
            client (httpx.AsyncClient): An asynchronous HTTP client used to make requests.
            user (User): A dictionary containing user registration data.

        Raises:
            Exception: If an error occurs during the signup process.

        Returns:
            None
        """
        try: 
            username = user["username"]
            resp = await client.post(f'{API_URL}/users', json=user)
            logger.info(f"[AUTH USER]: receive {resp.status_code} when signing up {username}")
        except Exception as e:
            raise Exception(e)
            
    async def login_user(self, client, user: User):
        """
        Login a user by sending a POST request to the user login endpoint.

        Args:
            client (httpx.AsyncClient): An asynchronous HTTP client used to make requests.
            user (User): A dictionary containing user login data.

        Raises:
            Exception: If an error occurs during the login process.

        Returns:
            str: The authentication token received upon successful login.
        """
        try:
            username = user["username"]
            resp = await client.post(f'{API_URL}/users/login', json=user)
            logger.info(f"[AUTH USER]: receive {resp.status_code} when logging in {username}")
            token = resp.json()["token"]
            return token
        except Exception as e:
            raise Exception(e)
            
    async def auth_user(self, client, user: User):
        """
        Authenticates a user with the API server.
        
        Args:
            user (dict): User information including username and password.
            client: An asynchronous client for making requests.
        
        Returns:
            str: Authentication token if authentication is successful.
        
        Notes:
            This function signs up and logs in a user, obtaining an authentication token from the server.
            Logs information about the process.
        """
        try:
            await self.signup_user(client, user)
            token = await self.login_user(client, user)
            if token:
                return token
        except Exception as e:
            logger.error(f"[AUTH USER]: {e}") 
            return None