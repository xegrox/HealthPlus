from flask_restful import Api

from .admin.staff_account import AdminStaffAccount
from .admin.staff_account_list import AdminStaffAccountList
from .admin.user_account import AdminUserAccount
from .admin.user_account_list import AdminUserAccountList
from .doctor.appointment import DoctorAppointment
from .doctor.appointment_list import DoctorAppointmentList
from .doctor.available_medicine import DoctorAvailableMedicine
from .doctor.available_timeslot_list import DoctorAvailableTimeslotList
from .session import SessionManagement
from .account import AccountManagement
from .pharmacist.medicine import PharmacistMedicine
from .pharmacist.medicine_list import PharmacistMedicineList
from .pharmacist.order_status import PharmacistOrderStatus
from .user.appointment import UserAppointment
from .user.appointment_list import UserAppointmentList
from .user.available_doctors import UserAvailableDoctors
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
    # added PharmacistOrderStatus class :D
    api.add_resource(PharmacistOrderStatus, '/user_medicine_order/<user_id>/<order_id>')
    api.add_resource(UserMedicineOrderList, '/medicine_order')
    api.add_resource(UserMedicineOrder, '/medicine_order/<order_id>')
    api.add_resource(UserAvailableMedicine, '/available_medicine')
    api.add_resource(UserAppointmentList, '/appointment')
    api.add_resource(UserAppointment, '/appointment/<appointment_id>')
    api.add_resource(UserAvailableDoctors, '/available_doctors')
    api.add_resource(VaccineOrderLogs, '/vaccine_logs')
    api.add_resource(DoctorAppointmentList, '/doctor_appointment')
    api.add_resource(DoctorAppointment, '/doctor_appointment/<appointment_id>')
    api.add_resource(DoctorAvailableMedicine, '/doctor_available_medicine')
    api.add_resource(DoctorAvailableTimeslotList, '/doctor_available_timeslot')
