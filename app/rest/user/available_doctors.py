from flask_login import login_required
from flask_restful import Resource

from app.database.accounts import staff_accounts
from app.models.account.staff import StaffRole


class UserAvailableDoctors(Resource):

    @staticmethod
    def __serialize_doctor(doctor):
        return {
            'doctor_id': doctor.get_id(),
            'name': 'Dr ' + doctor.full_name,
            'specialization': doctor.get_detail('specialization', ''),
            'description': doctor.get_detail('description', '')
        }

    @login_required
    def get(self):
        doctors = []
        for staff in staff_accounts.read_all():
            if staff.role is StaffRole.DOCTOR and staff.get_detail('public', True):
                doctors.append(self.__serialize_doctor(staff))
        return doctors, 200

