from datetime import datetime
from enum import Enum
from app.database import DatabaseObject


class VaccineType(Enum):
    PFIZER = 'Pfizer'
    MODERNA = 'Moderna'
    SINOVAC = 'Sinovac'


class VaccineLog(DatabaseObject):

    def __init__(self, batch_no, vaccine_type: VaccineType, quantity, delivery_date, expiry_date):
        self.batch_no = batch_no
        self.vaccine_type = vaccine_type
        self.quantity = quantity
        self.delivery_date = delivery_date
        self.expiry_date = expiry_date
        self.time_created = datetime.now()
        self.time_updated = datetime.now()

    @property
    def key(self) -> str:
        return self.batch_no
