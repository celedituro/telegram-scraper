import bcrypt

from ..models.exceptions import InvalidPassword

class Encrypter:
    def encrypt_password(self, password: str):
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            return hashed_password
        except Exception as e:
            raise InvalidPassword('the password must be a string')
    
    def check_password(self, plain_password: str, hashed_password: bytes):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)