from flask_restful import Resource, reqparse, abort

from app.database.accounts import staff_accounts
from app.database.exceptions import AccountAlreadyExistsError
from .utils import check_is_admin, serialize_staff
from app.models.account.staff import StaffRole


class AdminStaffAccountList(Resource):

    def get(self):
        check_is_admin()
        return list(map(serialize_staff, staff_accounts.read_all())), 200

    def post(self):
        check_is_admin()
        parser = reqparse.RequestParser(trim=True) \
            .add_argument('role', choices=(e.value for e in StaffRole), required=True) \
            .add_argument('staff_id', required=True) \
            .add_argument('first_name', required=True) \
            .add_argument('last_name', required=True) \
            .add_argument('password', trim=False, required=True)
        args = parser.parse_args()
        try:
            user = staff_accounts.create(args['role'], args['staff_id'], args['first_name'], args['last_name'], args['password'])
            return serialize_staff(user), 200
        except AccountAlreadyExistsError:
            abort(409)
