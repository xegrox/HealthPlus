from flask_login import current_user
from flask_restful import abort

from app.database.pharmacist import medicine_inventory
from app.models.account import User


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


def serialize_medicine_order(order):

    def fill_medicine_info(medicine_id, quantity):
        medicine = medicine_inventory.read(medicine_id)
        quantity_filled = serialize_medicine(medicine)
        quantity_filled['quantity'] = quantity
        return quantity_filled

    medicines = [fill_medicine_info(k, v) for k, v in order.quantities.items()]
    return {
        'order_id': order.order_id,
        'date': {
            'day': order.date.day,
            'month': order.date.month,
            'year': order.date.year
        },
        'medicines': medicines,
        'status': order.status
    }
