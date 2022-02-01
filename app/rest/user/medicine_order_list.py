from flask_login import login_required, current_user
from flask_restful import Resource, abort, reqparse
from app.database.exceptions import MedicineNotFoundError
from app.database.user import medicine_orders
from app.models.user_medicine_order import UserMedicineOrderMethod
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
        parser = reqparse.RequestParser(trim=True) \
            .add_argument('method', choices=(e.value for e in UserMedicineOrderMethod), required=True) \
            .add_argument('quantities', type=dict, required=True)
        args = parser.parse_args()
        try:
            quantities = {k: int(v) for k, v in args['quantities'].items()}
            order = medicine_orders.create(current_user.get_id(), quantities, args['method'])
            return serialize_medicine_order(order), 200
        except (ValueError, MedicineNotFoundError):
            abort(400)
