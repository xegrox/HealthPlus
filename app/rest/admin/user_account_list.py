from flask_restful import Resource, reqparse, abort

from app.database.accounts import user_accounts
from app.database.exceptions import AccountAlreadyExistsError, AccountNotFoundError
from .utils import check_is_admin, serialize_user


class AdminUserAccountList(Resource):

    def get(self):
        check_is_admin()
        return list(map(serialize_user, user_accounts.read_all())), 200

    def post(self):
        check_is_admin()
        parser = reqparse.RequestParser(trim=True) \
            .add_argument('nric', required=True) \
            .add_argument('first_name', required=True) \
            .add_argument('last_name', required=True) \
            .add_argument('password', trim=False, required=True)
        args = parser.parse_args()
        try:
            user = user_accounts.create(args['nric'], args['first_name'], args['last_name'], args['password'])
            return serialize_user(user), 200
        except AccountAlreadyExistsError:
            abort(409)

    def delete(self):
        check_is_admin()
        parser = reqparse.RequestParser(trim=True).add_argument('account_id', action='append', required=True)
        args = parser.parse_args()
        try:
            for account_id in args['account_id']:
                user_accounts.delete(account_id=account_id)
            return '', 200
        except AccountNotFoundError:
            abort(404)
