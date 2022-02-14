from uuid import uuid4

from app.database import Database, BasicDatabase
from app.database.exceptions import AppointmentNotFoundError
from app.database.utils import has_one_of, check_user_exists, check_staff_exists
from app.models.account.staff import StaffRole
from app.models.appointment import Appointment, AppointmentStatus

#   Appointments_db
#   +-------------------------------+
#   | appointment_id | appointment |
#   +----------------+-------------+
appointments_db = Database('appointments', keyerror=AppointmentNotFoundError)

#   Account map
#   +------------+------------------------+
#   | account_id | [appointment_id, ...] |
#   +-----------+------------------------+
appointments_user_map_db = BasicDatabase('appointments_user_map')
appointments_doctor_map_db = BasicDatabase('appointments_doctor_map')


# Either doctor_id or user_id has to be specified
# If appointment_id is specified: run operation on single appointment of account
# If appointment_id is not specified: run operation on every appointment of account
def __operation(delegate, doctor_id, user_id, appointment_id, *args):
    has_one_of(doctor_id, user_id)
    if doctor_id is not None:
        check_staff_exists(doctor_id, StaffRole.DOCTOR)
        appointments_map_db = appointments_doctor_map_db
        account_id = doctor_id
    if user_id is not None:
        check_user_exists(user_id)
        appointments_map_db = appointments_user_map_db
        account_id = user_id
    with appointments_map_db.open() as appointments_map:
        appointment_ids = appointments_map.get(account_id, set())
    if appointment_id is not None:
        if appointment_id not in appointment_ids:
            raise AppointmentNotFoundError(appointment_id)
        return delegate(appointment_id, account_id, *args)
    else:
        result = []
        for appointment_id in appointment_ids:
            result.append(delegate(appointment_id, account_id, *args))
        return result


def __read(appointment_id, _):
    with appointments_db.open() as appointments:
        appointment = appointments[appointment_id]
        if appointment.prescription is None:
            appointment.prescription = {}
        return appointment


def __update(appointment_id, _, status: AppointmentStatus = None, prescription=None):
    with appointments_db.open() as appointments:
        appointment = appointments[appointment_id]
        if status is not None:
            appointment.update_status(status)
        if appointment.status == AppointmentStatus.SEEN:
            appointment.prescription = prescription
        appointments.put(appointment)
    return appointment


def __delete(appointment_id, account_id):
    with appointments_db.open() as appointments:
        appointment = appointments[appointment_id]
        with appointments_doctor_map_db.open() as appointments_doctor_map:
            doctor_appointment_ids = appointments_doctor_map[appointment.doctor_id]
            doctor_appointment_ids.remove(appointment_id)
            appointments_doctor_map[account_id] = doctor_appointment_ids
        with appointments_user_map_db.open() as appointments_user_map:
            user_appointment_ids = appointments_user_map[appointment.user_id]
            user_appointment_ids.remove(appointment_id)
            appointments_user_map[account_id] = user_appointment_ids
        appointments.remove(appointment_id)


def create(doctor_id, user_id, datetime, condition, description):
    check_staff_exists(doctor_id, StaffRole.DOCTOR)
    check_user_exists(user_id)
    appointment = Appointment(uuid4().hex, doctor_id, user_id, datetime, condition, description)
    with appointments_db.open() as appointments:
        appointments.put(appointment)
        with appointments_user_map_db.open() as appointments_user_map:
            user_appointment_ids = appointments_user_map.get(user_id, set())
            user_appointment_ids.add(appointment.appointment_id)
            appointments_user_map[user_id] = user_appointment_ids
        with appointments_doctor_map_db.open() as appointments_doctor_map:
            doctor_appointment_ids = appointments_doctor_map.get(doctor_id, set())
            doctor_appointment_ids.add(appointment.appointment_id)
            appointments_doctor_map[doctor_id] = doctor_appointment_ids
    return appointment


def read(doctor_id=None, user_id=None, appointment_id=None):
    return __operation(__read, doctor_id, user_id, appointment_id)


def update(doctor_id=None, user_id=None, appointment_id=None, status=None, prescription=None):
    return __operation(__update, doctor_id, user_id, appointment_id, status, prescription)


def delete(doctor_id=None, user_id=None, appointment_id=None):
    __operation(__delete, doctor_id, user_id, appointment_id)
