import json
from abc import ABC


class Account(ABC):
    def __init__(self, account_id, first_name, last_name, password_hash):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash

    def serialize(self):
        return json.dumps(self)
