from flask_login import login_required, current_user
from flask_restful import Resource, abort
from app.database.appointments import appointments
from app.database.exceptions import AppointmentNotFoundError
from .utils import check_is_user, serialize_appointment


class UserAppointment(Resource):

    @login_required
    def get(self, appointment_id):
        check_is_user()
        try:
            return serialize_appointment(appointments.read(user_id=current_user.get_id(), appointment_id=appointment_id)), 200
        except AppointmentNotFoundError as e:
            abort(404, description=f'Appointment with id "{e.appointment_id}" not found')

    @login_required
    def delete(self, appointment_id):
        check_is_user()
        try:
            appointments.delete(user_id=current_user.get_id(), appointment_id=appointment_id)
        except AppointmentNotFoundError as e:
            abort(404, description=f'Appointment with id "{e.appointment_id}" not found')
