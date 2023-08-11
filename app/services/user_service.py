import base64

from datetime import datetime

from ..models.exceptions import UserAlreadyExist, UserNotFound, IncorrectPassword
from ..models.user import User

class UserService:
    def __init__(self, repository, encrypter, presenter):
        self.repository = repository
        self.encrypter = encrypter
        self.presenter = presenter

    def add_user(self, user: User):
        user_got = self.repository.get_user(user.username)
        if user_got is None:
            hashed_password = self.encrypter.encrypt_password(user.password)
            hashed_password_str = hashed_password.decode('utf-8')
            new_user = self.repository.insert_user(user.username, hashed_password_str)
            return self.presenter.present_user(new_user)
        raise UserAlreadyExist("The user already exist")
    
    def login_user(self, user: User):
        user_got = self.repository.get_user(user.username)
        if user_got is not None:
            hashed_password = user_got[1].encode('utf-8')
            if self.encrypter.check_password(user.password, hashed_password) is False:
                raise IncorrectPassword("The password is incorrect")
            else:
                return user_got
        raise UserNotFound("The user does not exist")
