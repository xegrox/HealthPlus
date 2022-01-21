from flask import request
from flask_restful import Resource, abort, reqparse

from .utils import check_is_admin, serialize_user
from app.database.accounts import user_accounts
from app.database.exceptions import AccountNotFoundError, AccountAlreadyExistsError


class AdminUserAccount(Resource):

    def get(self, account_id):
        check_is_admin()
        try:
            return serialize_user(user_accounts.read(account_id)), 200
        except AccountNotFoundError:
            abort(404)

    def put(self, account_id):
        check_is_admin()
        parser = reqparse.RequestParser(trim=True) \
            .add_argument('nric') \
            .add_argument('first_name') \
            .add_argument('last_name') \
            .add_argument('password', trim=False)
        args = parser.parse_args()
        try:
            return serialize_user(user_accounts.update(account_id=account_id, data=args)), 200
        except AccountNotFoundError:
            abort(404)
        except AccountAlreadyExistsError:
            abort(409)

    def delete(self, account_id):
        check_is_admin()
        try:
            user_accounts.delete(account_id=account_id)
            return 200
        except AccountNotFoundError:
            abort(404)
