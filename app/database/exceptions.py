class AccountAlreadyExistsError(Exception):
    ...


class AccountNotFoundError(Exception):
    ...


class UserNotFoundError(AccountNotFoundError):
    ...


class StaffNotFoundError(AccountNotFoundError):
    ...


class OrderNotFoundError(Exception):
    ...


class MedicineNotFoundError(Exception):
    ...


class AppointmentNotFoundError(Exception):
    def __init__(self, appointment_id):
        self.appointment_id = appointment_id
