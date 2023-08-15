import bcrypt

from ..exceptions.user_exceptions import InvalidPassword

class Encrypter:
    """
    A class responsible for password encryption and verification using bcrypt.

    Methods:
        encrypt_password(password: str): Encrypts a password using bcrypt.
        check_password(plain_password: str, hashed_password: bytes): Verifies a plain password against a hashed password.

    Notes:
        This class assists in securely encrypting and verifying passwords using the bcrypt hashing algorithm.
    """
    
    def encrypt_password(self, password: str):
        """
        Encrypts a password using bcrypt.

        Args:
            password (str): The plain text password to be encrypted.

        Returns:
            bytes: The hashed password.

        Raises:
            InvalidPassword: If the password is not a string.
        
        Notes:
            This method uses the bcrypt library to generate a salt and hash the provided password.
            It returns the hashed password suitable for storage.
        """
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            return hashed_password
        except Exception as e:
            raise InvalidPassword('the password must be a string')
    
    def check_password(self, plain_password: str, hashed_password: bytes):
        """
        Verifies a plain password against a hashed password.

        Args:
            plain_password (str): The plain text password to be verified.
            hashed_password (bytes): The hashed password to compare against.

        Returns:
            bool: True if the passwords match, False otherwise.

        Notes:
            This method uses bcrypt to compare the provided plain password with the stored hashed password.
            It returns a boolean value indicating whether the passwords match.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)