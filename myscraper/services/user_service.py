from datetime import datetime
    
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def add_user(self, user):
        return self.user_repository.insert_user(user.username, user.password)


