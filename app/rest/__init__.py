from flask_restful import Api
from .session import SessionManagement
from .account import AccountManagement
from .pharmacist.medicine import PharmacistMedicine
from .pharmacist.medicine_list import PharmacistMedicineList


def register_api(app):
    api = Api(app)
    api.add_resource(AccountManagement, '/account')
    api.add_resource(SessionManagement, '/session')
    api.add_resource(PharmacistMedicine, '/medicine/<medicine_id>')
    api.add_resource(PharmacistMedicineList, '/medicine')
