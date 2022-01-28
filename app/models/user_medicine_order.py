import datetime


class UserMedicineOrderStatus:
    PENDING = 'pending'
    ONGOING = 'ongoing'
    SENT = 'sent'


class UserMedicineOrder:
    def __init__(self, order_id: str, user_account_id: str, medicine_name, quantities: dict, method, collection_date):
        self._order_id = order_id
        self._user_account_id = user_account_id
        self._medicine_name = medicine_name
        self._quantities = quantities
        self._order_date = datetime.date.today()
        self._method = method
        self._status = UserMedicineOrderStatus.PENDING
        self._collection_date = collection_date

    @property
    def order_id(self): return self._order_id

    @property
    def user_account_id(self): return self._user_account_id

    @property
    def medicine_name(self): return self._medicine_name

    @property
    def quantities(self): return self._quantities

    @property
    def order_date(self): return self._order_date

    @property
    def method(self): return self._method

    @property
    def status(self): return self._status

    def update_status(self, status: UserMedicineOrderStatus): self._status = status

    @property
    def collection_date(self): return self._collection_date
