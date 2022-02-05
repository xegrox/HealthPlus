from datetime import datetime
from enum import Enum
from app.database import DatabaseObject


class TimeSlot(Enum):
    FOUR = '4'
    FIVE = '5'
    SIX = '6'


class VaccineType(Enum):
    PFIZER = 'Pfizer'
    MODERNA = 'Moderna'
    SINOVAC = 'Sinovac'


class NewAppointment(DatabaseObject):

    def __init__(self, date_of_birth, dose, vaccine_type: VaccineType, date_of_appointment, time_slot: TimeSlot):
        self.date_of_birth = date_of_birth
        self.dose = dose
        self.vaccine_type = vaccine_type
        self.date_of_appointment = date_of_appointment
        self.time_slot = time_slot
        self.time_created = datetime.now()
        self.time_updated = datetime.now()

    @property
    def key(self) -> str:
        return self.batch_no
