from flask import Flask
from flask_login import LoginManager

from app.database.accounts.exceptions import AccountAlreadyExistsError
from app.rest import register_api
from app.blueprints import home, dashboard
from app.database.accounts import user_accounts, staff_accounts

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.static_folder = 'static/dist'
register_api(app)
app.register_blueprint(home)
app.register_blueprint(dashboard)

login_manager = LoginManager()
login_manager.init_app(app)

# Temporary hard code staff accounts
try:
    staff_accounts.create('admin', 'admin', 'John', 'Smith', '123')
    staff_accounts.create('doctor', 'doctor', 'John', 'Smith', '123')
    staff_accounts.create('pharmacist', 'pharmacist', 'John', 'Smith', '123')
    staff_accounts.create('vaccine_manager', 'vaccine_manager', 'John', 'Smith', '123')
except AccountAlreadyExistsError:
    ...


@login_manager.user_loader
def load_account(account_id):
    if account_id[0] == 'U':
        return user_accounts.read(account_id=account_id)
    elif account_id[0] == 'S':
        return staff_accounts.read(account_id=account_id)
