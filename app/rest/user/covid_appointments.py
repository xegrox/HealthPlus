from flask_login import login_required
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from .utils import check_is_user, serialize_covid_appointment
from app.database.user import covid_appointments
from ...models.covid_appointment import VaccineType, Time


class CovidAppointments(Resource):

    @login_required
    def get(self):
        check_is_user()
        return list(map(serialize_covid_appointment, covid_appointments.read_all())), 200

    @login_required
    def post(self):
        parser = RequestParser() \
            .add_argument('date_of_birth', required=True) \
            .add_argument('dose', required=True) \
            .add_argument('vaccine_type', choices=(e.value for e in VaccineType), required=True) \
            .add_argument('date_of_appointment', required=True) \
            .add_argument('time', choices=(e.value for e in Time), required=True)
        args = parser.parse_args()
        appointment = covid_appointments.create(
            date_of_birth=args['date_of_birth'],
            dose=args['dose'],
            vaccine_type=args['vaccine_type'],
            date_of_appointment=args['date_of_appointment'],
            time=args['time']
        )
        return serialize_covid_appointment(appointment), 200

    @login_required
    def delete(self):
        check_is_user()
        parser = RequestParser().add_argument('date_of_birth', required=True, action='append')
        args = parser.parse_args()
        print(args['date_of_birth'])
        for date_of_birth in args['date_of_birth']:
            covid_appointments.delete(date_of_birth)
        return '', 200
