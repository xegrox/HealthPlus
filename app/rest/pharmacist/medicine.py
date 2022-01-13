from flask_restful import Resource, abort, reqparse

from app.database.exceptions import MedicineNotFoundError
from app.database.pharmacist import medicine_inventory


class PharmacistMedicine(Resource):

    def get(self, medicine_id):
        try:
            return medicine_inventory.read(medicine_id).serializable, 200
        except MedicineNotFoundError:
            abort(404)

    def put(self, medicine_id):
        parser = reqparse.RequestParser().add_argument('quantity', type=int, required=True)
        args = parser.parse_args()
        try:
            return medicine_inventory.update(medicine_id, args['quantity']).serializable, 200
        except MedicineNotFoundError:
            abort(404)

    def delete(self, medicine_id):
        try:
            medicine_inventory.delete(medicine_id)
            return '', 200
        except MedicineNotFoundError:
            abort(404)
