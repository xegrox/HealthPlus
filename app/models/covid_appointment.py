from datetime import datetime
from enum import Enum
from app.database import DatabaseObject


class Time(Enum):
    FOUR = 'Four'
    FIVE = 'Five'
    SIX = 'Six'


class VaccineType(Enum):
    PFIZER = 'Pfizer'
    MODERNA = 'Moderna'
    SINOVAC = 'Sinovac'


class NewAppointment(DatabaseObject):

    def __init__(self, date_of_birth, dose, vaccine_type: VaccineType, date_of_appointment, time: Time):
        self.date_of_birth = date_of_birth
        self.dose = dose
        self.vaccine_type = vaccine_type
        self.date_of_appointment = date_of_appointment
        self.time = time


    @property
    def key(self) -> str:
        return self.date_of_birth
