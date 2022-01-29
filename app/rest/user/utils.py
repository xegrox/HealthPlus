from flask_login import current_user
from flask_restful import abort

from app.database.pharmacist import medicine_inventory
from app.models.account import User
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


def serialize_medicine_order(order: UserMedicineOrder):

    def fill_medicine_info(medicine_id, quantity):
        medicine = medicine_inventory.read(medicine_id)
        quantity_filled = serialize_medicine(medicine)
        quantity_filled['quantity'] = quantity
        return quantity_filled

    quantities = [fill_medicine_info(k, v) for k, v in order.quantities.items()]
    return {
        'method': order.method.value,
        'order_id': order.order_id,
        'date': {
            'day': order.order_date.day,
            'month': order.order_date.month,
            'year': order.order_date.year
        },
        'quantities': quantities,
        'status': order.status.value
    }
