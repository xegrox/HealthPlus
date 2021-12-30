from flask import Flask
from flask_restful import Api
from app.rest import UserAccountList, UserAccount
from app.blueprints import home

app = Flask(__name__)
app.static_folder = 'static/dist'

api = Api(app)
api.add_resource(UserAccountList, '/users')
api.add_resource(UserAccount, '/users/<account_id>')

app.register_blueprint(home)
