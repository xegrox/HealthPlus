from hashlib import sha256
from app.database import user_accounts, DatabaseInterface
from flask_restful import Resource, abort, reqparse
from app.models.account.user import User
from .utils.generate_id import generate_user_id

parser = reqparse.RequestParser(trim=True)
parser.add_argument('first_name', required=True)
parser.add_argument('last_name', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


class UserAccountList(Resource):
    def get(self):
        with user_accounts.open() as db:
            users = list(map(lambda x: vars(x), db.values()))
            return users, 200

    def post(self):
        with user_accounts.open() as db:
            args = parser.parse_args()
            existing_ids = db.keys()
            while (account_id := generate_user_id()) in existing_ids:
                ...
            user = User(
                account_id=account_id,
                first_name=args['first_name'],
                last_name=args['last_name'],
                email=args['email'],
                password_hash=sha256(args['password'].encode()).hexdigest()
            )
            db.put(user)
            return vars(user), 200


def abort_if_user_not_exists(interface: DatabaseInterface, account_id):
    if not interface.exists(account_id):
        abort(404, message=f'User "{account_id}" does not exists')


class UserAccount(Resource):
    def get(self, account_id):
        with user_accounts.open() as db:
            abort_if_user_not_exists(db, account_id)
            user = db.get(account_id)
            return vars(user), 200

    def put(self, account_id):
        with user_accounts.open() as db:
            abort_if_user_not_exists(db, account_id)
            user = db.get(account_id)
            args = parser.parse_args()
            if val := args['first_name']:
                user.first_name = val
            if val := args['last_name']:
                user.last_name = val
            if val := args['email']:
                user.email = val
            if val := args['password']:
                user.password_hash = sha256(val.encode()).hexdigest()
            db.put(user)
            return vars(user), 200

    def delete(self, account_id):
        with user_accounts.open() as db:
            abort_if_user_not_exists(db, account_id)
            db.remove(account_id)
            return '', 200
