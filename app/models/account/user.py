from .account import Account


class User(Account):

    def __init__(self, account_id, nric: str, first_name, last_name, password_hash):
        super().__init__(account_id, first_name, last_name, password_hash)
        self.nric = nric

    @property
    def serializable(self):
        return {
            'nric': self.nric,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
