from flask_login import login_required, current_user
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.database.appointments import appointments
from .utils import check_is_doctor, serialize_appointment
from app.models.appointment import AppointmentStatus


class DoctorAppointmentList(Resource):

    @login_required
    def get(self):
        check_is_doctor()
        return [serialize_appointment(a) for a in appointments.read(doctor_id=current_user.get_id())], 200

    @login_required
    def put(self):
        check_is_doctor()
        parser = RequestParser() \
            .add_argument('appointment_id', action='append', required=True) \
            .add_argument('status', choices=(e.value for e in AppointmentStatus), required=True)
        args = parser.parse_args()
        for appointment_id in args['appointment_id']:
            appointments.update(
                status=AppointmentStatus(args['status']),
                doctor_id=current_user.get_id(),
                appointment_id=appointment_id
            )
        return '', 200
