from flask_login import current_user
from flask_restful import abort

from app.database.accounts import user_accounts
from app.models.account import Staff
from app.models.account.staff import StaffRole
from app.models.appointment import Appointment


def check_is_doctor():
    if not isinstance(current_user, Staff) or current_user.role != StaffRole.DOCTOR:
        abort(401)


def serialize_appointment(appointment: Appointment):
    patient_name = user_accounts.read(appointment.user_id).full_name
    return {
        'appointment_id': appointment.appointment_id,
        'patient_name': patient_name,
        'status': appointment.status.value,
        'datetime': appointment.datetime.isoformat(),
        'condition': appointment.condition,
        'description': appointment.description
    }


def serialize_medicine(medicine):
    return {
        'medicine_id': medicine.medicine_id,
        'name': medicine.name,
        'description': medicine.description,
        'atc_code': medicine.atc_code
    }
