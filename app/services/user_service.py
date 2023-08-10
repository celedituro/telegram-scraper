from datetime import datetime

from ..models.exceptions import UserAlreadyExist, UserNotFound
 
class UserService:
    def __init__(self, repository, encrypter, presenter):
        self.repository = repository
        self.encrypter = encrypter
        self.presenter = presenter

    def add_user(self, user):
        hashed_password = self.encrypter.encrypt_password(user.password)
        if self.repository.get_user(user.username) is None:
            new_user = self.repository.insert_user(user.username, hashed_password)
            return self.presenter.present_user(new_user)
        raise UserAlreadyExist("The user already exist")
    
    def login_user(self, user):
        user_got = self.repository.get_user(user.username)
        if user_got is not None:
            return user_got
        raise UserNotFound("The user does not exist")
