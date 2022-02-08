from enum import Enum
from .account import Account


class StaffRole(Enum):
    ADMIN = 'admin'
    DOCTOR = 'doctor'
    PHARMACIST = 'pharmacist'
    VACCINE_MANAGER = 'vaccine_manager'


class Staff(Account):
    def __init__(self, account_id, role: StaffRole, staff_id: str, first_name, last_name, password_hash):
        super().__init__(account_id, first_name, last_name, password_hash)
        self.role = role
        self.staff_id = staff_id
        self.__details = {}

    def put_detail(self, name, value):
        self.__details[name] = value

    def get_detail(self, name, default=None):
        return self.__details.get(name, default)

    @property
    def serializable(self):
        return {
            'role': self.role.value,
            'staff_id': self.staff_id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
