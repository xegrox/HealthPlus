from flask import Flask
from flask_login import LoginManager
from app.rest import register_api
from app.blueprints import home, dashboard
from app.database.accounts import user_accounts

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.static_folder = 'static/dist'
register_api(app)
app.register_blueprint(home)
app.register_blueprint(dashboard)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_account(account_id):
    return user_accounts.read(account_id=account_id)
