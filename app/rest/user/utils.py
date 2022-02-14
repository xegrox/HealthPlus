from flask_login import current_user
from flask_restful import abort
from app.database.accounts import staff_accounts
from app.database.pharmacist import medicine_inventory
from app.models.account import User
from app.models.appointment import Appointment
from app.models.user_medicine_order import UserMedicineOrder



def check_is_user():
    if not isinstance(current_user, User):
        abort(401)


def serialize_medicine(medicine):
    return {
        'medicine_id': medicine.medicine_id,
        'name': medicine.name,
        'description': medicine.description,
        'atc_code': medicine.atc_code
    }


def serialize_covid_appointment(covid_appointments):
    return {
        'date_of_birth': covid_appointments.date_of_birth,
        'dose': covid_appointments.dose,
        'vaccine_name': covid_appointments.vaccine_type.value,
        'date_of_appointment': covid_appointments.date_of_appointment,
        'time_name': covid_appointments.time.value
    }


def fill_medicine_info(medicine_id, quantity):
    medicine = medicine_inventory.read(medicine_id)
    quantity_filled = serialize_medicine(medicine)
    quantity_filled['quantity'] = quantity
    return quantity_filled


def serialize_medicine_order(order: UserMedicineOrder):
    quantities = [fill_medicine_info(k, v) for k, v in order.quantities.items()]
    return {
        'method': order.method.value,
        'order_id': order.order_id,
        'user_account_id': order.user_account_id,
        'date': {
            'day': order.order_date.day,
            'month': order.order_date.month,
            'year': order.order_date.year
        },
        'quantities': quantities,
        'status': order.status.value
    }


def serialize_appointment(appointment: Appointment):
    doctor_name = 'Dr ' + staff_accounts.read(appointment.doctor_id).full_name
    return {
        'appointment_id': appointment.appointment_id,
        'doctor_name': doctor_name,
        'status': appointment.status.value,
        'datetime': appointment.datetime.isoformat(),
        'condition': appointment.condition,
        'description': appointment.description,
        'prescription': [fill_medicine_info(k, v) for k, v in appointment.prescription.items()]
    }
