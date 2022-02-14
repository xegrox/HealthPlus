from flask import request
from flask_login import login_required, current_user
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from app.database.appointments import appointments
from app.database.exceptions import AppointmentNotFoundError
from .utils import check_is_doctor, serialize_appointment


class DoctorAppointment(Resource):

    @login_required
    def get(self, appointment_id):
        check_is_doctor()
        try:
            return serialize_appointment(appointments.read(doctor_id=current_user.get_id(), appointment_id=appointment_id)), 200
        except AppointmentNotFoundError as e:
            abort(404, description=f'Appointment with id "{e.appointment_id}" not found')

    @login_required
    def put(self, appointment_id):
        check_is_doctor()
        try:
            prescription = {e[0]: int(e[1]) for e in request.json.items()}
            appointments.update(doctor_id=current_user.get_id(), appointment_id=appointment_id, prescription=prescription)
            return '', 200
        except ValueError:
            abort(400)
        except AppointmentNotFoundError as e:
            abort(404, description=f'Appointment with id "{e.appointment_id}" not found')