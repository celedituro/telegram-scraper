class InvalidPassword(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UserNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)