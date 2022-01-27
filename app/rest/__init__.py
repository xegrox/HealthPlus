from flask_restful import Api

from .admin.staff_account import AdminStaffAccount
from .admin.staff_account_list import AdminStaffAccountList
from .admin.user_account import AdminUserAccount
from .admin.user_account_list import AdminUserAccountList
from .session import SessionManagement
from .account import AccountManagement
from .pharmacist.medicine import PharmacistMedicine
from .pharmacist.medicine_list import PharmacistMedicineList
from .user.available_medicine import UserAvailableMedicine
from .user.medicine_order import UserMedicineOrder
from .user.medicine_order_list import UserMedicineOrderList
from .vaccine_manager.vaccine_order_logs import VaccineOrderLogs


def register_api(app):
    api = Api(app)
    api.add_resource(AccountManagement, '/account')
    api.add_resource(SessionManagement, '/session')
    api.add_resource(AdminUserAccountList, '/user_account')
    api.add_resource(AdminUserAccount, '/user_account/<account_id>')
    api.add_resource(AdminStaffAccountList, '/staff_account')
    api.add_resource(AdminStaffAccount, '/staff_account/<account_id>')
    api.add_resource(PharmacistMedicineList, '/medicine')
    api.add_resource(PharmacistMedicine, '/medicine/<medicine_id>')
    api.add_resource(UserMedicineOrderList, '/medicine_order')
    api.add_resource(UserMedicineOrder, '/medicine_order/<order_id>')
    api.add_resource(UserAvailableMedicine, '/available_medicine')
    api.add_resource(VaccineOrderLogs, '/vaccine_logs')
