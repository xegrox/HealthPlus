from app.database import Database
from app.models.covid_appointment import Time, VaccineType, NewAppointment

covid_appointments_db = Database('covid_appointments')


def read_all():
    with covid_appointments_db.open() as covid_appointments:
        return list(covid_appointments.values())


def read(date_of_birth):
    with covid_appointments_db.open() as covid_appointments:
        return covid_appointments[date_of_birth]


def create(date_of_birth, dose, vaccine_type, date_of_appointment, time):
    appointment = NewAppointment(date_of_birth, dose, VaccineType(vaccine_type), date_of_appointment, Time(time))
    with covid_appointments_db.open() as covid_appointments:
        covid_appointments.put(appointment)
        return appointment


def delete(date_of_birth):
    with covid_appointments_db.open() as covid_appointments:
        covid_appointments.remove(date_of_birth)
