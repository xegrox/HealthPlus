from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.account import User, Staff
from app.models.account.staff import StaffRole
from app.rest.admin.staff_account_list import AdminStaffAccountList
from app.rest.admin.user_account_list import AdminUserAccountList
from app.rest.doctor.appointment_list import DoctorAppointmentList
from app.rest.doctor.available_timeslot_list import DoctorAvailableTimeslotList
from app.rest.pharmacist.medicine_list import PharmacistMedicineList
from app.rest.user.appointment_list import UserAppointmentList
from app.rest.user.available_doctors import UserAvailableDoctors
from app.rest.user.available_medicine import UserAvailableMedicine
from app.rest.user.medicine_order_list import UserMedicineOrderList
from app.rest.vaccine_manager.vaccine_order_logs import VaccineOrderLogs

blueprint = Blueprint(
    'dashboard', __name__,
    template_folder='templates',
    static_folder='static'
)


class _Page:
    def __init__(self, name: str, icon: str, fragment: str, template: str, right_panel_template: str = None):
        self.name = name
        self.icon = icon
        self.fragment = fragment
        self.template = template
        self.right_panel_template = right_panel_template


# doctor - available_timeslots
@blueprint.route('/ajax/doctor/settings/available_timeslots_section', methods=['POST'])
def doctor_available_timeslots():
    timeslots = DoctorAvailableTimeslotList().get()[0]
    return render_template('/dashboard/doctor/settings/available_timeslots_section.html', timeslots=timeslots)


# doctor - appointments
@blueprint.route('/ajax/doctor/appointments/appointments_table', methods=['POST'])
def doctor_appointments_table():
    appointments = DoctorAppointmentList().get()[0]
    return render_template('/dashboard/doctor/appointments/appointments_table.html', appointments=appointments)


# vaccine_manager
@blueprint.route('/ajax/vaccine_manager/log_history/vaccine_log_table', methods=['POST'])
def log_info():
    logs = VaccineOrderLogs().get()[0]
    return render_template('/dashboard/vaccine_manager/log_history/vaccine_log_table.html', logs=logs)


# pharmacist - inventory
@blueprint.route('/ajax/pharmacist/inventory/inventory_base', methods=['POST'])
def medicine_management():
    medicines = PharmacistMedicineList().get()[0]
    return render_template('/dashboard/pharmacist/inventory/inventory_base.html', medicines=medicines)


# user - prescriptions
@blueprint.route('/ajax/user/prescriptions/prescription_list', methods=['POST'])
def prescription_list():
    appointments = UserAppointmentList().get()[0]
    return render_template('/dashboard/user/prescriptions/prescription_list.html', appointments=appointments)


# pharmacist - collection status
@blueprint.route('/ajax/pharmacist/collection_status/patient_orders', methods=['POST'])
def patient_orders():
    orders = UserMedicineOrderList().get()[0]
    return render_template('/dashboard/pharmacist/collection_status/patient_orders.html', orders=orders)


# user - order medicine
@blueprint.route('/ajax/user/order_medicine/medicine_table', methods=['POST'])
def medicine_list():
    medicines = UserAvailableMedicine().get()[0]
    return render_template('/dashboard/user/order_medicine/medicine_table.html', medicines=medicines)


# user - order history
@blueprint.route('/ajax/user/order_history/order_table', methods=['POST'])
def display_order():
    orders = UserMedicineOrderList().get()[0]
    return render_template('/dashboard/user/order_history/order_table.html', orders=orders)


# user - appointments
@blueprint.route('/ajax/user/appointments/appointments_table', methods=['POST'])
def user_appointments_table():
    appointments = UserAppointmentList().get()[0]
    return render_template('/dashboard/user/appointments/appointments_table.html', appointments=appointments)


@blueprint.route('/ajax/user/appointments/available_doctors_table', methods=['POST'])
def user_available_doctors_table():
    doctors = UserAvailableDoctors().get()[0]
    return render_template('/dashboard/user/appointments/available_doctors_table.html', doctors=doctors)


@blueprint.route('/ajax/user/appointments/available_timeslots_grid', methods=['POST'])
def user_available_timeslots_grid():
    timeslots = [('09', '30'), ('09', '45'), ('10', '15'), ('11', '45'), ('12', '30')]
    return render_template('/dashboard/user/appointments/available_timeslots_grid.html', timeslots=timeslots)


@blueprint.route('/ajax/admin/manage_staffs/accounts_table', methods=['POST'])
@login_required
def admin_staff_accounts_table():
    if isinstance(current_user, Staff) and current_user.role == StaffRole.ADMIN:
        accounts = AdminStaffAccountList().get()[0]
        return render_template('dashboard/admin/manage_staffs/accounts_table.html', accounts=accounts)


@blueprint.route('/ajax/admin/manage_users/accounts_table', methods=['POST'])
@login_required
def admin_user_accounts_table():
    if isinstance(current_user, Staff) and current_user.role == StaffRole.ADMIN:
        accounts = AdminUserAccountList().get()[0]
        return render_template('dashboard/admin/manage_users/accounts_table.html', accounts=accounts)


@blueprint.route('/')
@login_required
def dashboard():
    if isinstance(current_user, User):
        return render_template('dashboard/index.html', pages=[
            _Page('Appointments', 'calendar-event', 'appointments', 'dashboard/user/appointments/index.html'),
            _Page('Covid Appointments', 'vaccine', 'covid_appointment', 'dashboard/user/covid_appointment/index.html'),
            _Page('Prescriptions', 'prescription', 'prescriptions', 'dashboard/user/prescriptions/index.html'),
            _Page('Order Medicine', 'medicine-syrup', 'order_medicine', 'dashboard/user/order_medicine/index.html', 'dashboard/user/order_medicine/right_panel.html'),
            _Page('Order History', 'history', 'order_history', 'dashboard/user/order_history/index.html'),
            _Page('Settings', 'settings', 'settings', 'dashboard/user/settings/index.html')
        ])
    elif isinstance(current_user, Staff):
        if current_user.role == StaffRole.ADMIN:
            return render_template('dashboard/index.html', pages=[
                _Page('Manage staff', 'friends', 'manage_staffs', 'dashboard/admin/manage_staffs/index.html'),
                _Page('Manage users', 'users', 'manage_users', 'dashboard/admin/manage_users/index.html'),
                _Page('Settings', 'settings', 'settings', 'dashboard/admin/settings/index.html')
            ])
        elif current_user.role == StaffRole.DOCTOR:
            return render_template('dashboard/index.html', pages=[
                _Page('Appointments', 'calendar-event', 'appointments', 'dashboard/doctor/appointments/index.html', 'dashboard/doctor/appointments/right_panel.html'),
                _Page('Settings', 'settings', 'settings', 'dashboard/doctor/settings/index.html')
            ])
        elif current_user.role == StaffRole.PHARMACIST:
            return render_template('dashboard/index.html', pages=[
                _Page('Collection Status', 'truck', 'collection_status', 'dashboard/pharmacist/collection_status/index.html'),
                _Page('Settings', 'settings', 'settings', 'dashboard/pharmacist/settings/index.html'),
                _Page('Inventory', 'pencil', 'inventory_management', 'dashboard/pharmacist/inventory/index.html')
            ])
        elif current_user.role == StaffRole.VACCINE_MANAGER:
            return render_template('dashboard/index.html', pages=[
                _Page('Vaccine Log', 'notebook', 'log_history', 'dashboard/vaccine_manager/log_history/index.html'),
                _Page('Settings', 'settings', 'settings', 'dashboard/vaccine_manager/settings/index.html'),

            ])
