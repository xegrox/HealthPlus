from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.account import User, Staff
from app.models.account.staff import StaffRole

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


@blueprint.route('/')
@login_required
def dashboard():
    if isinstance(current_user, User):
        return render_template('dashboard/index.html', pages=[
            _Page('Appointments', 'calendar-event', 'appointments', 'dashboard/user/appointments/index.html'),
            _Page('Prescriptions', 'prescription', 'prescriptions', 'dashboard/user/prescriptions/index.html'),
            _Page('Settings', 'settings', 'settings', 'dashboard/user/settings/index.html')
        ])
    elif isinstance(current_user, Staff):
        if current_user.role == StaffRole.ADMIN:
            return render_template('dashboard/index.html', pages=[
                _Page('Settings', 'settings', 'settings', 'dashboard/admin/settings/index.html')
            ])
        elif current_user.role == StaffRole.DOCTOR:
            return render_template('dashboard/index.html', pages=[
                _Page('Settings', 'settings', 'settings', 'dashboard/doctor/settings/index.html')
            ])
        elif current_user.role == StaffRole.PHARMACIST:
            return render_template('dashboard/index.html', pages=[
                _Page('Settings', 'settings', 'settings', 'dashboard/pharmacist/settings/index.html')
            ])
        elif current_user.role == StaffRole.VACCINE_MANAGER:
            return render_template('dashboard/index.html', pages=[
                _Page('Settings', 'settings', 'settings', 'dashboard/vaccine_manager/settings/index.html')
            ])
