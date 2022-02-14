import datetime
from enum import Enum


class UserMedicineOrderMethod(Enum):
    DELIVERY = 'delivery'
    COLLECTION = 'collection'


class UserMedicineOrderStatus(Enum):
    PENDING = 'pending'
    ONGOING = 'ongoing'
    AVAILABLE = 'available'
    CANCELLED = "cancelled"


class UserMedicineOrder:
    def __init__(self, order_id: str, user_account_id: str, quantities: dict, method: UserMedicineOrderMethod):
        self._order_id = order_id
        self._user_account_id = user_account_id
        self._quantities = quantities
        self._order_date = datetime.date.today()
        self._method = method
        self._status = UserMedicineOrderStatus.PENDING

    @property
    def order_id(self): return self._order_id

    @property
    def user_account_id(self): return self._user_account_id

    @property
    def quantities(self): return self._quantities

    @property
    def order_date(self): return self._order_date

    @property
    def method(self): return self._method

    @property
    def status(self): return self._status

    def update_status(self, status: UserMedicineOrderStatus): self._status = status
