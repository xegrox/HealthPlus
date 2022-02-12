from flask_login import login_required
from flask_restful import Resource

from app.database.pharmacist import medicine_inventory
from .utils import serialize_medicine, check_is_doctor


class DoctorAvailableMedicine(Resource):

    @login_required
    def get(self):
        check_is_doctor()
        serialized = [serialize_medicine(med) for med in medicine_inventory.read_all()]
        return serialized, 200
