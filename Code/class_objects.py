# Copied from Robert's repo #
class User:
    def __init__(self, username, password, first_name=None, middle_name=None, last_name=None, email=None, password_confirmation=None):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.password_confirmation = password_confirmation