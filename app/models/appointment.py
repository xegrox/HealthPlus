import uuid
from enum import Enum

from app.database.database_object import DatabaseObject


class AppointmentMethod(Enum):
    online = 1
    physical = 2


class Appointment(DatabaseObject):
    def __init__(self, doctor_id, user_id, method, datetime):
        self.uuid = str(uuid.uuid4())
        self.doctor_id = doctor_id
        self.user_id = user_id
        self.method = method
        self.datetime = datetime

    def key(self) -> str:
        return self.uuid
