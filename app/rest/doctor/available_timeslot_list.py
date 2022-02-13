import uuid

from flask_login import login_required, current_user
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app.database.accounts import staff_accounts
from app.rest.doctor.utils import check_is_doctor


class DoctorAvailableTimeslotList(Resource):

    @login_required
    def get(self):
        check_is_doctor()
        return current_user.get_detail('timeslots', {}), 200

    @login_required
    def post(self):
        check_is_doctor()
        parser = RequestParser() \
            .add_argument('day', choices=('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'), required=True) \
            .add_argument('start', required=True) \
            .add_argument('end', required=True)
        args = parser.parse_args()
        timeslots = current_user.get_detail('timeslots', {})
        day_timeslots = timeslots.get(args['day'], {})
        day_timeslots[uuid.uuid4().hex] = {
            'start': args['start'],
            'end': args['end']
        }
        timeslots[args['day']] = day_timeslots
        staff_accounts.update(account_id=current_user.get_id(), data={
            'details': {'timeslots': timeslots}
        })
        return '', 200

    @login_required
    def delete(self):
        check_is_doctor()
        parser = RequestParser() \
            .add_argument('day', choices=('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'), required=True) \
            .add_argument('timeslot_id', required=True)
        args = parser.parse_args()
        timeslots = current_user.get_detail('timeslots', {})
        del timeslots[args['day']][args['timeslot_id']]
        staff_accounts.update(account_id=current_user.get_id(), data={
            'details': {'timeslots': timeslots}
        })
