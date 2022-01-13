from flask_restful import Resource

from app.database.pharmacist import medicine_inventory
from .utils import serialize_medicine


class UserAvailableMedicine(Resource):

    def get(self):
        serialized = [serialize_medicine(med) for med in medicine_inventory.read_all()]
        return serialized, 200
