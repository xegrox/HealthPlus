from flask_login import current_user
from flask_restful import abort

from app.models.account import Staff
from app.models.account.staff import StaffRole


def check_is_pharmacist():
    if not isinstance(current_user, Staff) or current_user.role != StaffRole.PHARMACIST:
        abort(401)
