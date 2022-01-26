from flask_login import current_user
from flask_restful import abort

from app.models.account import Staff
from app.models.account.staff import StaffRole


def check_is_vaccine_manager():
    if not isinstance(current_user, Staff) or current_user.role != StaffRole.VACCINE_MANAGER:
        abort(401)


def serialize_log(log):
    return {
        'vaccine_name': log.vaccine_type.value,
        'batch_no': log.batch_no,
        'quantity': log.quantity,
        'delivery_date': log.delivery_date,
        'expiry_date': log.expiry_date
    }