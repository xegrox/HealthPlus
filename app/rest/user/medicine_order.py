from flask_login import login_required, current_user
from flask_restful import Resource, abort

from app.database.user import medicine_orders
from .utils import serialize_medicine_order, check_is_user
from ...database.exceptions import OrderNotFoundError
from ...models.user_medicine_order import UserMedicineOrderStatus


class UserMedicineOrder(Resource):

    @login_required
    def get(self, order_id):
        check_is_user()
        try:
            order = medicine_orders.read(current_user.get_id(), order_id)
            return serialize_medicine_order(order), 200
        except OrderNotFoundError:
            abort(404)

    @login_required
    def delete(self, order_id):
        check_is_user()
        try:
            order = medicine_orders.read(current_user.get_id(), order_id)
            if order.status != UserMedicineOrderStatus.PENDING:
                abort(403)
            medicine_orders.delete(current_user.get_id(), order_id)
            return '', 200
        except OrderNotFoundError:
            abort(404)
