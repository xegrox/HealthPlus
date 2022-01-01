from .database import Database, DatabaseInterface
from .database_object import DatabaseObject, BasicDatabaseObject

user_accounts = Database('user_accounts')
user_emails_map = Database('user_emails_map')
