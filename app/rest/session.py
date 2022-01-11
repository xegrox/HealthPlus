from hashlib import sha256
from flask_login import login_user, logout_user, login_required
from flask_restful import Resource, reqparse, abort
from app.database.accounts import user_accounts

parser = reqparse.RequestParser(trim=True)
parser.add_argument('nric', required=True)
parser.add_argument('password', required=True)


class SessionManagement(Resource):

    def post(self):
        args = parser.parse_args()
        nric = args['nric']
        password = args['password']
        # Verify password and login
        try:
            user = user_accounts.read(nric=nric)
            password_hash = sha256(password.encode()).hexdigest()
            if password_hash != user.password_hash:
                abort(401)
            login_user(user)
            return '', 200, {'HX-Refresh': "true"}
        except user_accounts.UserNotFoundError:
            abort(401)

    @login_required
    def delete(self):
        logout_user()
        return '', 200, {'HX-Redirect': "/"}
