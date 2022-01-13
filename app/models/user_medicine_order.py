import datetime


class UserMedicineOrderStatus:
    PENDING = 'pending'
    ONGOING = 'ongoing'
    SENT = 'sent'


class UserMedicineOrder:
    def __init__(self, order_id: str, user_account_id: str, quantities: dict):
        self._order_id = order_id
        self._user_account_id = user_account_id
        self._date = datetime.date.today()
        self._quantities = quantities
        self._status = UserMedicineOrderStatus.PENDING

    @property
    def order_id(self): return self._order_id

    @property
    def user_account_id(self): return self._user_account_id

    @property
    def date(self): return self._date

    @property
    def quantities(self): return self._quantities

    @property
    def status(self): return self._status

    def update_status(self, status: UserMedicineOrderStatus): self._status = status
