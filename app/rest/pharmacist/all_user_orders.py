from flask_login import login_required
from flask_restful import Resource

from app.rest.user.utils import serialize_medicine_order
from app.database.user import medicine_orders
from .utils import check_is_pharmacist


class PharmacistAllOrdersList(Resource):

    @login_required
    def get(self):
        check_is_pharmacist()
        orders = list(medicine_orders.read_all())
        serialized = [serialize_medicine_order(order) for order in orders]
        return serialized, 200
