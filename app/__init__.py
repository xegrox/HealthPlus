from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from app.rest import UserAccountList, UserAccount, UserSessions
from app.blueprints import home
from app.database import user_accounts

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.static_folder = 'static/dist'
app.register_blueprint(home)

api = Api(app)
api.add_resource(UserAccountList, '/users')
api.add_resource(UserAccount, '/users/<account_id>')
api.add_resource(UserSessions, '/user_sessions')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_account(account_id):
    with user_accounts.open() as db:
        return db.get(account_id)
