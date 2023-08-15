import base64

from datetime import datetime

from ..exceptions.user_exceptions import UserAlreadyExist, UserNotFound, IncorrectPassword
from ..models.data_models import User
from ..database.repositories.user_respository import UserRepository
from ..models.encrypter import Encrypter
from ..models.user_presenter import UserPresenter

class UserService:
    """
    A class responsible for managing operations related to users.

    Args:
        repository (UserRepository): An instance of the UserRepository class for database operations.
        encrypter (Encrypter): An instance of the Encrypter class for password encryption and verification.
        presenter (UserPresenter): An instance of the UserPresenter class for data presentation.

    Attributes:
        repository (UserRepository): The user repository instance.
        encrypter (Encrypter): The encrypter instance for password handling.
        presenter (UserPresenter): The user presenter instance.

    Methods:
        add_user(user: User): Adds a user to the database.
        login_user(user: User): Authenticates a user's login credentials.

    Notes:
        This class provides methods to manage users, including registration and authentication.
    """
    
    def __init__(self, repository: UserRepository, encrypter: Encrypter, presenter: UserPresenter):
        """
        Initializes the UserService class with a user repository, encrypter, and presenter.

        Args:
            repository (UserRepository): An instance of the UserRepository class for database operations.
            encrypter (Encrypter): An instance of the Encrypter class for password encryption and verification.
            presenter (UserPresenter): An instance of the UserPresenter class for data presentation.
        """
        self.repository = repository
        self.encrypter = encrypter
        self.presenter = presenter

    def add_user(self, user: User):
        """
        Adds a user to the database.

        Args:
            user (User): The user to be added.

        Returns:
            dict: The added user information.

        Raises:
            UserAlreadyExist: If the user already exists in the database.

        Notes:
            This method checks if the user already exists. If not, it inserts the user into the database
            with encrypted password and returns the added user information. Otherwise, it raises an exception.
        """
        user_got = self.repository.get_user(user.username)
        if user_got is None:
            hashed_password = self.encrypter.encrypt_password(user.password)
            hashed_password_str = hashed_password.decode('utf-8')
            new_user = self.repository.insert_user(user.username, hashed_password_str)
            return self.presenter.present_user(new_user)
        raise UserAlreadyExist("The user already exist")
    
    def login_user(self, user: User):
        """
        Authenticates a user's login credentials.

        Args:
            user (User): The user's login credentials.

        Returns:
            tuple: The user information if authentication is successful.

        Raises:
            IncorrectPassword: If the provided password is incorrect.
            UserNotFound: If the user does not exist in the database.

        Notes:
            This method checks the user's credentials and verifies the password. If successful, it returns
            the user information. Otherwise, it raises appropriate exceptions.
        """
        user_got = self.repository.get_user(user.username)
        if user_got is not None:
            hashed_password = user_got[1].encode('utf-8')
            if self.encrypter.check_password(user.password, hashed_password) is False:
                raise IncorrectPassword("The password is incorrect")
            else:
                return user_got
        raise UserNotFound("The user does not exist")
