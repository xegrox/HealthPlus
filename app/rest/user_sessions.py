from hashlib import sha256
from flask_login import login_user, logout_user, login_required
from flask_restful import Resource, reqparse, abort
from app.database import user_emails_map, user_accounts

parser = reqparse.RequestParser(trim=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


class UserSessions(Resource):

    def post(self):
        args = parser.parse_args()
        email = args['email']
        password = args['password']
        # Get account id of email
        with user_emails_map.open() as db:
            if email not in db.keys():
                abort(401)
            else:
                account_id = db.get(email).value
        # Verify password and login
        with user_accounts.open() as db:
            user = db.get(account_id)
            password_hash = sha256(password.encode()).hexdigest()
            if password_hash != user.password_hash:
                abort(401)
            else:
                login_user(user)
                return '', 200, {'HX-Refresh': "true"}

    @login_required
    def delete(self):
        logout_user()
        return '', 200, {'HX-Refresh': "true"}
