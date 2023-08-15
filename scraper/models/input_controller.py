from loguru import logger

class InputController:
    """
    A class for validating user credentials.
    """
    
    def get_user_credentials(self):
        """
        This function prompts the user for a username and password,
        and returns a dictionary containing these values.

        Returns:
        dict: A dictionary with the user credentials in the following format:
            {
                "username": <username>,
                "password": <password>
            }
        """
        try:
            username = input('Username: ')
            password = input('Password: ')

            if not username or not password:
                raise ValueError("Both username and password must have a value.")

            user = {
                "username": username,
                "password": password
            }
            logger.info("[INPUT CONTROLLER]: user credentials got")
            return user
        except Exception as e:
            logger.error(f"[INPUT CONTROLLER]: {e}")
            return None