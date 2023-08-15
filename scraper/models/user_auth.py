from loguru import logger
import sys
sys.path.append("..")

from api.models.data_models import User

class UserAuth:
    async def signup_user(self, client, user: User):
        try: 
            username = user["username"]
            resp = await client.post('http://localhost:8000/users', json=user)
            logger.info(f"[AUTH USER]: receive {resp.status_code} when signing up {username}")
        except Exception as e:
            logger.error(f"[AUTH USER]: {e}")
            raise Exception("Error when signing up user")
            
    async def login_user(self, client, user: User):
        try:
            username = user["username"]
            resp = await client.post('http://localhost:8000/users/login', json=user)
            logger.info(f"[AUTH USER]: receive {resp.status_code} when logging in {username}")
            token = resp.json()["token"]
            return token
        except Exception as e:
            logger.error(f"[AUTH USER]: {e}")
            raise Exception("Error when logging in user")
            
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