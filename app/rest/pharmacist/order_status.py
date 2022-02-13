from flask_login import login_required
from flask_restful import Resource, abort, reqparse

from app.database.user import medicine_orders
from .utils import check_is_pharmacist
from ...database.exceptions import OrderNotFoundError
from ...models.user_medicine_order import UserMedicineOrderStatus


class PharmacistOrderStatus(Resource):

    @login_required
    def put(self, user_id, order_id):
        check_is_pharmacist()
        order = medicine_orders.read(user_id, order_id)
        parser = reqparse.RequestParser().add_argument('status', choices=(e.value for e in UserMedicineOrderStatus), required=True)
        args = parser.parse_args()
        if order.status != UserMedicineOrderStatus.CANCELLED:
            try:
                return medicine_orders.update(user_id, order_id, args['status']).serializable, 200
            except OrderNotFoundError:
                abort(404)
