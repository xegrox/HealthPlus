from flask import request
from flask_login import login_required, current_user
from flask_restful import Resource, abort

from app.database.user import medicine_orders
from app.rest.user.utils import check_is_user, serialize_medicine_order


class UserMedicineOrderList(Resource):

    @login_required
    def get(self):
        check_is_user()
        orders = list(medicine_orders.read(current_user.get_id()).values())
        serialized = [serialize_medicine_order(order) for order in orders]
        return serialized, 200

    @login_required
    def post(self):
        check_is_user()
        try:
            parsed_order = {med_id: int(quantity) for med_id, quantity in request.form.items()}
            order = medicine_orders.create(current_user.get_id(), parsed_order)
            return serialize_medicine_order(order), 200
        except ValueError:
            abort(400)
