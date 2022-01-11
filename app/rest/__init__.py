from flask_restful import Api
from .session import SessionManagement
from .account import AccountManagement


def register_api(app):
    api = Api(app)
    api.add_resource(AccountManagement, '/account')
    api.add_resource(SessionManagement, '/session')
