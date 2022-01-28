from datetime import datetime
from enum import Enum
from app.database import DatabaseObject


class MedicineType(Enum):
    A = 'Amlodipine'
    F = 'Fluoxetine (Prozac)'


class MedicineOrder(DatabaseObject):

    def __init__(self, order_id, medicine_type: MedicineType, quantity, collection_date):
        self.order_id = order_id
        self.medicine_type = medicine_type
        self.quantity = quantity
        self.collection_date = collection_date

    @property
    def key(self) -> str:
        return self.order_id