import sys
sys.path.append("..")
from loguru import logger

from scraper.utils.constants import API_URL

REDIRECTION_STATUS_CODE = 307

class MessageHandler:
    """
    A class for handling messages.
    """
        
    async def handle_response(self, client, response):
        """
        Handles the response from an API server after posting a message.
        
        Args:
            client: An asynchronous client used to make requests.
            response: The response received from the API server.
            
        Notes:
            If the response status code indicates redirection, the function will follow
            the redirection by sending a POST request to the new location.
        """
        try:
            while response.status_code == REDIRECTION_STATUS_CODE:
                new_location = response.headers.get('Location')
                logger.info(f'[MESSAGE HANDLER]: redirecting request to: {new_location}')
                response = await client.post(new_location, json=data)
            logger.info(f"[MESSAGE HANDLER]: receive {response.status_code}")
        except Exception as e:
            raise Exception(e)

    async def post_message(self, client, parsed_message, token: str):
        """
        Posts a parsed message to a server.
        
        Args:
            client: An asynchronous client used to make requests.
            message: A parsed messages to be posted.
            token (str): Authentication token for the server.
        """
        try:
            id = parsed_message["id"]
            logger.info(f'[MESSAGE HANDLER]: post message {id}')
            response = await client.post(f'{API_URL}/messages', json=parsed_message, headers={"Authorization": f"Bearer {token}"})
            await self.handle_response(client, response)
        except Exception as e:
            raise Exception(e)
                        
    async def post_messages(self, client, parsed_messages, token: str):
        """
        Posts parsed messages to a server.
        
        Args:
            client: An asynchronous client used to make requests.
            parsed_messages (list): List of parsed messages to be posted.
            token (str): Authentication token for the server.
        
        Notes:
            This function iterates through the parsed messages, sends each message to the server with the
            authentication token, and handles the server's response using the handle_response function.
        """
        try:
            for parsed_message in parsed_messages:
                if parsed_message:
                    await self.post_message(client, parsed_message, token)
        except Exception as e:
            logger.error(f"[MESSAGE HANDLER]: {e}") 
            raise Exception(e)  