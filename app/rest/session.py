from flask_login import login_user, logout_user, login_required
from flask_restful import Resource, reqparse, abort
from app.database.accounts import user_accounts, staff_accounts
from app.database.accounts.exceptions import AccountNotFoundError
from .utils import hash_sha256

parser = reqparse.RequestParser(trim=True)
parser.add_argument('nric')
parser.add_argument('staff_id')
parser.add_argument('password', trim=False, required=True)


class SessionManagement(Resource):

    def post(self):
        args = parser.parse_args()
        nric = args['nric']
        staff_id = args['staff_id']
        password = args['password']
        if all({nric, staff_id}) or not any({nric, staff_id}):
            # Abort if both nric and staff_id are specified
            # Abort if neither nric nor staff_id is specified
            abort(400)
        try:
            account = user_accounts.read(nric=nric) if nric \
                else staff_accounts.read(staff_id=staff_id)
            # Verify password and login
            if hash_sha256(password) != account.password_hash:
                abort(401)
            login_user(account)
            return '', 200, {'HX-Refresh': "true"}
        except AccountNotFoundError:
            abort(401)

    @login_required
    def delete(self):
        logout_user()
        return '', 200, {'HX-Redirect': "/"}
