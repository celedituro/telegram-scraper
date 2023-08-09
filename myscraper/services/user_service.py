from datetime import datetime
    
class UserService:
    def __init__(self, repository, encrypter, presenter):
        self.repository = repository
        self.encrypter = encrypter
        self.presenter = presenter

    def add_user(self, user):
        hashed_password = self.encrypter.encrypt_password(user.password)
        new_user = self.repository.insert_user(user.username, hashed_password)
        return self.presenter.present_user(new_user)
    
    def login_user(self, user):
        return self.repository.get_user(user.username)
