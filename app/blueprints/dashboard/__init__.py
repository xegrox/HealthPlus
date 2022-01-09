from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.account.user import Patient

blueprint = Blueprint(
    'dashboard', __name__,
    template_folder='templates'
)


class _Page:
    def __init__(self, name: str, icon: str, fragment: str, template: str):
        self.name = name
        self.icon = icon
        self.fragment = fragment
        self.template = template


@blueprint.route('/dashboard')
@login_required
def dashboard():
    if isinstance(current_user, Patient):
        return render_template('dashboard/index.html', pages=[
            _Page('Appointments', 'calendar-event', 'appointments', 'dashboard/patient/appointments/index.html'),
            _Page('Prescriptions', 'prescription', 'prescriptions', 'dashboard/patient/prescriptions/index.html'),
            _Page('Settings', 'settings', 'settings', 'dashboard/patient/settings/index.html')
        ])
