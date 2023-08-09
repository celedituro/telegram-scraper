class UserPresenter:
    def present_user(self, user):
        new_user = {
            "username": user[0],
            "hashed_password": user[1],
        }
        return new_user