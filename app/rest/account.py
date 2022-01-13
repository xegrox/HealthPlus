from flask_login import login_required, current_user, logout_user
from flask_restful import Resource, reqparse, abort
from app.database.accounts import user_accounts, staff_accounts
from app.database.exceptions import AccountAlreadyExistsError
from app.models.account.user import User
from app.models.account.staff import Staff
from .utils import hash_sha256


class AccountManagement(Resource):

    def __database_of_account(self, account):
        if isinstance(account, User):
            return user_accounts
        elif isinstance(account, Staff):
            return staff_accounts

    # Post method is for creating users only; staff is created by admin
    def post(self):
        parser = reqparse.RequestParser(trim=True) \
            .add_argument('nric', required=True) \
            .add_argument('first_name', required=True) \
            .add_argument('last_name', required=True) \
            .add_argument('password', trim=False, required=True)
        args = parser.parse_args()
        try:
            user = user_accounts.create(args['nric'], args['first_name'], args['last_name'], args['password'])
            return user.serializable, 200
        except AccountAlreadyExistsError:
            abort(409)

    @login_required
    def get(self):
        database = self.__database_of_account(current_user)
        account = database.read(account_id=current_user.get_id())
        return account.serializable, 200

    @login_required
    def put(self):
        if isinstance(current_user, User):
            parser = reqparse.RequestParser(trim=True) \
                .add_argument('first_name') \
                .add_argument('last_name') \
                .add_argument('password', trim=False)
        else:
            # Staff can only change password
            parser = reqparse.RequestParser() \
                .add_argument('password')
        args = parser.parse_args()
        database = self.__database_of_account(current_user)
        try:
            account = database.update(account_id=current_user.get_id(), data=args)
            return account.serializable, 200
        except AccountAlreadyExistsError:
            abort(409)

    @login_required
    def delete(self):
        if isinstance(current_user, User):
            parser = reqparse.RequestParser().add_argument('password', required=True)
            args = parser.parse_args()
            if hash_sha256(args['password']) != current_user.password_hash:
                abort(401)
            user_accounts.delete(account_id=current_user.get_id())
            logout_user()
            return '', 200, {'HX-Redirect': "/"}
        else:
            # Staff cannot delete account
            abort(401)
