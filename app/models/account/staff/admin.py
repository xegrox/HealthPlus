from .staff import Staff


class Admin(Staff):
    def __init__(self, account_id, first_name, last_name, password_hash):
        super().__init__(account_id, first_name, last_name, password_hash)
