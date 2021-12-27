from app.models.account.account import Account


class User(Account):

    def __init__(self, account_id, first_name, last_name, email, password_hash):
        super().__init__(account_id, first_name, last_name, password_hash)
        self.email = email

