from flask_login import current_user
from flask_restful import abort

from app.models.account import Staff
from app.models.account.staff import StaffRole


def check_is_admin():
    if not isinstance(current_user, Staff) or current_user.role != StaffRole.ADMIN:
        abort(401)


def serialize_user(user):
    return {
        'account_id': user.get_id(),
        'nric': user.nric,
        'first_name': user.first_name,
        'last_name': user.last_name
    }


def serialize_staff(staff):
    return {
        'account_id': staff.get_id(),
        'staff_id': staff.staff_id,
        'role': staff.role.value,
        'first_name': staff.first_name,
        'last_name': staff.last_name
    }
