from datetime import datetime
    
class UserService:
    def __init__(self, user_repository, encrypter):
        self.user_repository = user_repository
        self.encrypter = encrypter

    def add_user(self, user):
        hashed_password = self.encrypter.encrypt_password(user.password)
        return self.user_repository.insert_user(user.username, hashed_password)
