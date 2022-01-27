from flask_restful import Resource, abort, reqparse
from .utils import check_is_admin, serialize_staff
from app.database.accounts import staff_accounts
from app.database.exceptions import AccountNotFoundError, AccountAlreadyExistsError


class AdminStaffAccount(Resource):

    def get(self, account_id):
        check_is_admin()
        try:
            return serialize_staff(staff_accounts.read(account_id)), 200
        except AccountNotFoundError:
            abort(404)

    def put(self, account_id):
        check_is_admin()
        parser = reqparse.RequestParser(trim=True) \
            .add_argument('role', choices=('admin', 'doctor', 'pharmacist', 'vaccine_manager')) \
            .add_argument('staff_id') \
            .add_argument('first_name') \
            .add_argument('last_name') \
            .add_argument('password', trim=False)
        args = parser.parse_args()
        try:
            return serialize_staff(staff_accounts.update(account_id=account_id, data=args)), 200
        except AccountNotFoundError:
            abort(404)
        except AccountAlreadyExistsError:
            abort(409)

    def delete(self, account_id):
        check_is_admin()
        try:
            staff_accounts.delete(account_id=account_id)
            return 200
        except AccountNotFoundError:
            abort(404)
