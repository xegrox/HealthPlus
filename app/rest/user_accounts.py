from hashlib import sha256
from app.database import user_accounts, DatabaseInterface
from flask_restful import Resource, abort, reqparse
from app.models.account.user import Patient


class UserAccountList(Resource):

    def get(self):
        with user_accounts.open() as db:
            users = list(map(lambda x: vars(x), db.values()))
            return users, 200

    def post(self):
        with user_accounts.open() as db:
            parser = reqparse.RequestParser(trim=True) \
                .add_argument('nric', required=True) \
                .add_argument('first_name', required=True) \
                .add_argument('last_name', required=True) \
                .add_argument('password', required=True)
            args = parser.parse_args()
            if args['nric'] in db.keys():
                abort(409)
            user = Patient(
                nric=args['nric'],
                first_name=args['first_name'],
                last_name=args['last_name'],
                password_hash=sha256(args['password'].encode()).hexdigest()
            )
            db.put(user)  # Add user account
            return vars(user), 200


def abort_if_user_not_exists(interface: DatabaseInterface, nric):
    if not interface.exists(nric):
        abort(404, message=f'User "{nric}" does not exists')


class UserAccount(Resource):
    def get(self, nric):
        with user_accounts.open() as db:
            abort_if_user_not_exists(db, nric)
            user = db.get(nric)
            return vars(user), 200

    def put(self, nric):
        with user_accounts.open() as db:
            abort_if_user_not_exists(db, nric)
            user = db.get(nric)
            parser = reqparse.RequestParser(trim=True) \
                .add_argument('first_name') \
                .add_argument('last_name') \
                .add_argument('password')
            args = parser.parse_args()
            if val := args.get('first_name'):
                user.first_name = val
            if val := args.get('last_name'):
                user.last_name = val
            if val := args.get('password'):
                user.password_hash = sha256(val.encode()).hexdigest()
                print(user.password_hash)
            db.put(user)
            return vars(user), 200

    def delete(self, nric):
        with user_accounts.open() as db:
            abort_if_user_not_exists(db, nric)
            db.remove(nric)
            return '', 200
