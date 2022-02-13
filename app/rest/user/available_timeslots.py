from flask_login import login_required
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from app.database.accounts import staff_accounts
from app.models.account.staff import StaffRole
from app.rest.user.utils import check_is_user


class UserAvailableTimeslotList(Resource):

    @login_required
    def get(self):
        check_is_user()
        parser = RequestParser() \
            .add_argument('doctor_id', required=True) \
            .add_argument('day', choices=('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'), required=True)
        args = parser.parse_args()
        doctor = staff_accounts.read(account_id=args['doctor_id'])
        if doctor.role != StaffRole.DOCTOR:
            abort(401)
        timeslots = doctor.get_detail('timeslots', {})
        return timeslots.get(args['day'], {}), 200
