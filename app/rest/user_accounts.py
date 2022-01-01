from hashlib import sha256
from app.database import user_accounts, user_emails_map, DatabaseInterface, BasicDatabaseObject
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
        with user_accounts.open() as accounts_db:
            with user_emails_map.open() as emails_map_db:
                args = parser.parse_args()
                email = args['email']
                if email in emails_map_db.keys():
                    abort(409)  # Abort if email already exists
                # Generate a unique account id
                existing_ids = accounts_db.keys()
                while (account_id := generate_user_id()) in existing_ids:
                    ...
                user = User(
                    account_id=account_id,
                    first_name=args['first_name'],
                    last_name=args['last_name'],
                    email=args['email'],
                    password_hash=sha256(args['password'].encode()).hexdigest()
                )
                accounts_db.put(user)  # Add user account
                item = BasicDatabaseObject(args['email'], account_id)
                emails_map_db.put(item)  # Map email to account id
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
                # Replace old email
                with user_emails_map.open() as _:
                    item = BasicDatabaseObject(val, account_id)
                    _.remove(user.email)
                    _.put(item)
                user.email = val
            if val := args['password']:
                user.password_hash = sha256(val.encode()).hexdigest()
                db.put(user)
                return vars(user), 200

    def delete(self, account_id):
        with user_accounts.open() as db:
            abort_if_user_not_exists(db, account_id)
            email = db.get(account_id).email
            db.remove(account_id)
            with user_emails_map.open() as _:
                _.remove(email)
            return '', 200
