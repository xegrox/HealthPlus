from .user import User


class Patient(User):
    def __init__(self, nric, first_name, last_name, password_hash):
        super().__init__(nric, first_name, last_name, password_hash)
