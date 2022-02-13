from datetime import datetime

from flask_login import login_required
from flask_restful import Resource, abort, inputs
from flask_restful.reqparse import RequestParser
from pytz import timezone

from app.database.accounts import staff_accounts
from app.models.account.staff import StaffRole
from app.rest.user.utils import check_is_user


class UserAvailableTimeslotList(Resource):

    @login_required
    def get(self):
        check_is_user()
        parser = RequestParser() \
            .add_argument('date', type=inputs.datetime_from_iso8601, required=True) \
            .add_argument('doctor_id', required=True)
        args = parser.parse_args()
        doctor = staff_accounts.read(account_id=args['doctor_id'])
        if doctor.role != StaffRole.DOCTOR:
            abort(401)
        date = args['date'].astimezone(timezone('Asia/Singapore')).date()
        day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][date.weekday()]
        timeslots = doctor.get_detail('timeslots', {}).get(day, {})
        for k, v in timeslots.copy().items():
            booked_dates = v.get('booked_dates', set())
            if date in booked_dates:
                del timeslots[k]
        return timeslots, 200
