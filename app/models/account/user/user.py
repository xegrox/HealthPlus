from ..account import Account


class User(Account):

    def __init__(self, nric, first_name, last_name, password_hash):
        super().__init__(nric, first_name, last_name, password_hash)
        self.nric = nric
