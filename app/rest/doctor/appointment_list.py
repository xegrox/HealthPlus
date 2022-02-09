from flask_login import login_required, current_user
from flask_restful import Resource, abort, reqparse, inputs
from app.database.appointments import appointments
from app.database.exceptions import AppointmentNotFoundError, StaffNotFoundError
from .utils import check_is_doctor, serialize_appointment


class DoctorAppointmentList(Resource):

    @login_required
    def get(self):
        check_is_doctor()
        return [serialize_appointment(a) for a in appointments.read(doctor_id=current_user.get_id())], 200
