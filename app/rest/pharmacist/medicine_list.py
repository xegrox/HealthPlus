from flask_login import login_required
from flask_restful import Resource, reqparse

from app.database.pharmacist import medicine_inventory
from .utils import check_is_pharmacist


class PharmacistMedicineList(Resource):

    @login_required
    def get(self):
        check_is_pharmacist()
        return list(map(lambda x: x.serializable, medicine_inventory.read_all()))

    @login_required
    def post(self):
        check_is_pharmacist()
        parser = reqparse.RequestParser() \
            .add_argument('atc_code') \
            .add_argument('name', required=True) \
            .add_argument('description', required=True) \
            .add_argument('license_holder', required=True) \
            .add_argument('quantity', type=int, required=True)
        args = parser.parse_args()
        return medicine_inventory.create(
            atc_code=args['atc_code'],
            name=args['name'],
            description=args['description'],
            license_holder=args['license_holder'],
            quantity=args['quantity']
        ).serializable, 200
