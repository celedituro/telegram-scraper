class InvalidToken(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ExpiredToken(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)