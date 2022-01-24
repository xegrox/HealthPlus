from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.account import User, Staff
from app.models.account.staff import StaffRole
from app.rest.admin.user_account_list import AdminUserAccountList
from app.rest.user.available_medicine import UserAvailableMedicine
from app.rest.user.medicine_order_list import UserMedicineOrderList

blueprint = Blueprint(
    'dashboard', __name__,
    template_folder='templates',
    static_folder='static'
)


class _Page:
    def __init__(self, name: str, icon: str, fragment: str, template: str):
        self.name = name
        self.icon = icon
        self.fragment = fragment
        self.template = template


@blueprint.route('/ajax/user/order_medicine/med_available', methods=['POST'])
def medicine_list():
    medicines = UserAvailableMedicine().get()[0]
    return render_template('/dashboard/user/order_medicine/med_available.html', medicines=medicines)


@blueprint.route('/ajax/user/order_history/orders_table', methods=['POST'])
def store_order():
    orders = UserMedicineOrderList().get()[0]
    return render_template('/dashboard/user/order_history/orders_table.html', orders=orders)


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
            _Page('Prescriptions', 'prescription', 'prescriptions', 'dashboard/user/prescriptions/index.html'),
            _Page('Order Medicine', 'medicine-syrup', 'order_medicine', 'dashboard/user/order_medicine/index.html'),
            _Page('Order History', 'history', 'order_history', 'dashboard/user/order_history/orders_table.html'),
            _Page('Settings', 'settings', 'settings', 'dashboard/user/settings/index.html')
        ])
    elif isinstance(current_user, Staff):
        if current_user.role == StaffRole.ADMIN:
            return render_template('dashboard/index.html', pages=[
                _Page('Manage users', 'users', 'manage_users', 'dashboard/admin/manage_users/index.html'),
                _Page('Settings', 'settings', 'settings', 'dashboard/admin/settings/index.html')
            ])
        elif current_user.role == StaffRole.DOCTOR:
            return render_template('dashboard/index.html', pages=[
                _Page('Settings', 'settings', 'settings', 'dashboard/doctor/settings/index.html')
            ])
        elif current_user.role == StaffRole.PHARMACIST:
            return render_template('dashboard/index.html', pages=[
                _Page('Collection Status', 'settings', 'collection_status', 'dashboard/pharmacist/collection_status/update_status.html'),
                _Page('Settings', 'settings', 'settings', 'dashboard/pharmacist/settings/index.html')
            ])
        elif current_user.role == StaffRole.VACCINE_MANAGER:
            return render_template('dashboard/index.html', pages=[
                _Page('Settings', 'settings', 'settings', 'dashboard/vaccine_manager/settings/index.html')
            ])
