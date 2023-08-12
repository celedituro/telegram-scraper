import bcrypt

from ..exceptions.user_exceptions import InvalidPassword

class Encrypter:
    """
    Encrypt a plaintext password.
    
    Args:
        password: plaintext password.
        
    Returns:
        Hash.
    """
    def encrypt_password(self, password: str):
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            return hashed_password
        except Exception as e:
            raise InvalidPassword('the password must be a string')
    
    """
    Checks if the plaintext password corresponds with the encrypted password.
    
    Args:
        plain_password: plaintext password.
        hashed_password: encrypted password.
        
    Returns:
        Bool.
    """
    def check_password(self, plain_password: str, hashed_password: bytes):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)