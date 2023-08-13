class UserPresenter:
    
    """
    Presents a user.
    
    Args:
        user: dictionary.
        
    Returns:
        A dictionary with username and password.
    """
    def present_user(self, user):
        new_user = {
            "username": user[0],
            "hashed_password": user[1],
        }
        return new_user
    
    def present_user_token(self, token):
        token = {
            "token": token
        }
        return token