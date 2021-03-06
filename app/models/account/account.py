from abc import ABCMeta
from flask_login import UserMixin
from app.database import DatabaseObject


class Account(DatabaseObject, UserMixin, metaclass=ABCMeta):
    def __init__(self, account_id: str, first_name: str, last_name: str, password_hash: str):
        self.__account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash

    @property
    def key(self) -> str:
        return self.__account_id

    def get_id(self):
        return self.__account_id

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    