from flask_login import login_required, current_user
from flask_restful import Resource, reqparse, abort
from app.models.account.user import User
from app.database.accounts import user_accounts


class AccountManagement(Resource):

    # Post method is for creating users only; staff is created by admin
    def post(self):
        parser = reqparse.RequestParser(trim=True) \
            .add_argument('nric', required=True) \
            .add_argument('first_name', required=True) \
            .add_argument('last_name', required=True) \
            .add_argument('password', required=True)
        args = parser.parse_args()
        try:
            user = user_accounts.create(args['nric'], args['first_name'], args['last_name'], args['password'])
            return user.serializable, 200
        except user_accounts.UserAlreadyExistsError:
            abort(409)

    @login_required
    def get(self):
        if isinstance(current_user, User):
            user = user_accounts.read(account_id=current_user.get_id())
            return user.serializable, 200

    @login_required
    def put(self):
        if isinstance(current_user, User):
            parser = reqparse.RequestParser(trim=True) \
                .add_argument('first_name') \
                .add_argument('last_name') \
                .add_argument('password')
            args = parser.parse_args()
            user = user_accounts.update(account_id=current_user.get_id(), data=args)
            return user.serializable, 200

    @login_required
    def delete(self):
        if isinstance(current_user, User):
            user_accounts.delete(account_id=current_user.get_id())
            return '', 200
