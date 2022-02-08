import datetime

from flask_login import login_required, current_user
from flask_restful import Resource, abort, reqparse, inputs
from app.database.appointments import appointments
from app.database.exceptions import AppointmentNotFoundError, StaffNotFoundError
from .utils import check_is_user, serialize_appointment


class UserAppointmentList(Resource):

    @login_required
    def get(self):
        check_is_user()
        return [serialize_appointment(a)for a in appointments.read(user_id=current_user.get_id())], 200

    @login_required
    def post(self):
        check_is_user()
        parser = reqparse.RequestParser() \
            .add_argument('doctor_id', required=True) \
            .add_argument('datetime', type=inputs.datetime_from_iso8601, required=True) \
            .add_argument('condition', required=True) \
            .add_argument('description', required=True)
        args = parser.parse_args()
        try:
            return serialize_appointment(appointments.create(
                user_id=current_user.get_id(),
                doctor_id=args['doctor_id'],
                datetime=args['datetime'],
                condition=args['condition'],
                description=args['description']
            )), 200
        except StaffNotFoundError:
            abort(404, description=f'Doctor with account id "{args["doctor_id"]}" not found')

    @login_required
    def delete(self):
        check_is_user()
        parser = reqparse.RequestParser().add_argument('appointment_id', append=True, required=True)
        args = parser.parse_args()
        try:
            for appointment_id in args['appointment_id']:
                appointments.delete(user_id=current_user.get_id(), appointment_id=appointment_id)
            return '', 200
        except AppointmentNotFoundError as e:
            abort(404, description=f'Appointment with id "{e.appointment_id}" not found')
