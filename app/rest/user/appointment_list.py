from flask_login import login_required, current_user
from flask_restful import Resource, abort, reqparse, inputs
from pytz import timezone
from app.database.appointments import appointments
from app.database.exceptions import AppointmentNotFoundError, StaffNotFoundError
from .utils import check_is_user, serialize_appointment
from app.database.accounts import staff_accounts


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
            .add_argument('timeslot_id', required=True) \
            .add_argument('date', type=inputs.datetime_from_iso8601, required=True) \
            .add_argument('condition', required=True) \
            .add_argument('description', required=True)
        args = parser.parse_args()
        try:
            timeslot_id = args['timeslot_id']
            timeslots = staff_accounts.read(account_id=args['doctor_id']).get_detail('timeslots')
            datetime = None
            for day, timeslot_ids in timeslots.items():
                if timeslot_id in timeslot_ids:
                    split = timeslot_ids[timeslot_id]['start'].split(':')
                    datetime = args['date'].astimezone(timezone('Asia/Singapore'))
                    datetime = datetime.replace(hour=int(split[0]), minute=int(split[1]))
                    booked_dates = timeslots[day][timeslot_id].get('booked_dates', set())
                    booked_dates.add(datetime.date())
                    timeslots[day][timeslot_id]['booked_dates'] = booked_dates
                    staff_accounts.update(account_id=args['doctor_id'], data={
                        'details': {'timeslots': timeslots}
                    })
                    break
            if datetime is None:
                abort(400)
            return serialize_appointment(appointments.create(
                user_id=current_user.get_id(),
                doctor_id=args['doctor_id'],
                datetime=datetime,
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
