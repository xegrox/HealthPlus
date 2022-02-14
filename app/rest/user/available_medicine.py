from flask_login import login_required, current_user
from flask_restful import Resource

from app.database.appointments import appointments
from .utils import check_is_user, fill_medicine_info
from app.database.user import medicine_orders


class UserAvailableMedicine(Resource):

    @login_required
    def get(self):
        check_is_user()
        available_medicines = {}
        for appointment in appointments.read(user_id=current_user.get_id()):
            for medicine_id, quantity in appointment.prescription.items():
                available_medicines[medicine_id] = available_medicines.get(medicine_id, 0) + quantity
        for order in medicine_orders.read(user_account_id=current_user.get_id()).values():
            for medicine_id, quantity in order.quantities.items():
                if medicine_id in available_medicines:
                    available_medicines[medicine_id] -= quantity
        return [fill_medicine_info(medicine_id, quantity) for medicine_id, quantity in available_medicines.items()], 200
