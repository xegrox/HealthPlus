from .user import User


class Patient(User):
    def __init__(self, account_id, first_name, last_name, email, password_hash, appointments):
        super().__init__(account_id, first_name, last_name, email, password_hash)
        self.__appointments = appointments

    def get_appointments(self):
        return self.__appointments

    def update_appointments(self, appointments):
        self.__appointments = appointments
