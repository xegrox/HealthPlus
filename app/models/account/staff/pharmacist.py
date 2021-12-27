from staff import Staff


class Pharmacist(Staff):
    def __init__(self, account_id, first_name, last_name, staff_id, password_hash):
        super().__init__(account_id, first_name, last_name, staff_id, password_hash)
