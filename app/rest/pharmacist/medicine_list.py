from pickle import APPEND
from pickletools import read_uint1
from flask_login import login_required
from flask_restful import Resource, abort, reqparse
from import_expression import parse
from app.database.exceptions import MedicineNotFoundError

from app.database.pharmacist import medicine_inventory
from .utils import check_is_pharmacist


class PharmacistMedicineList(Resource):

    @login_required
    def get(self):
        check_is_pharmacist()
        return list(map(lambda x: x.serializable, medicine_inventory.read_all())), 200

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

    @login_required
    def delete(self):
        check_is_pharmacist()
        parser = reqparse.RequestParser() \
            .add_argument('medicine_id', required=True, action='append')
        args = parser.parse_args()
        try:
            for medicine_id in args['medicine_id']:
                medicine_inventory.delete(medicine_id=medicine_id)
            return '', 200
        except MedicineNotFoundError:
            abort(404)
