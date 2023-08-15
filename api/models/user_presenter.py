class UserPresenter:
    """
    A class responsible for presenting user-related data.

    Methods:
        present_user(user): Creates a presentation-ready user dictionary.
        present_user_token(token): Creates a presentation-ready token dictionary.
    """
    
    def present_user(self, user):
        """
        Creates a presentation-ready user dictionary.

        Args:
            user (tuple): A tuple containing user information.

        Returns:
            dict: A dictionary with user information in a structured format.
        """
        new_user = {
            "username": user[0],
            "hashed_password": user[1],
        }
        return new_user
    
    def present_user_token(self, token):
        """
        Creates a presentation-ready token dictionary.

        Args:
            token (str): An authentication token.

        Returns:
            dict: A dictionary with the authentication token.
        """
        token = {
            "token": token
        }
        return token