from enum import Enum
from app.database.database_object import DatabaseObject


class AppointmentStatus(Enum):
    BOOKED = 'Booked'
    NO_SHOW = 'No Show'
    CANCELLED_BY_DOCTOR = 'Cancelled By Doctor'
    SEEN = 'Seen'

    def __str__(self):
        return self.value


class Appointment(DatabaseObject):
    def __init__(self, appointment_id, doctor_id, user_id, datetime, condition, description):
        self.appointment_id = appointment_id
        self.doctor_id = doctor_id
        self.user_id = user_id
        self.datetime = datetime
        self.condition = condition
        self.description = description
        self.__status = AppointmentStatus.BOOKED

    def update_status(self, status: AppointmentStatus):
        self.__status = status

    @property
    def status(self):
        return self.__status

    @property
    def key(self) -> str:
        return self.appointment_id
