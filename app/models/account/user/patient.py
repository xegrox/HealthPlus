from .user import User


class Patient(User):
    def __init__(self, nric, first_name, last_name, password_hash, appointments):
        super().__init__(nric, first_name, last_name, password_hash)
        self.__appointments = appointments

    def get_appointments(self):
        return self.__appointments

    def update_appointments(self, appointments):
        self.__appointments = appointments
