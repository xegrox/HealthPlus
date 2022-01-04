import json
import os
from app import app
import unittest


class TestUserInfoRestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()
        cls.user_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'nric': 'T0123456A',
            'password': 'secret',
            'password_hash': '2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b'
        }

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('user_accounts')

    def test_01_add_user(self):
        res = self.client.post('/users', data=self.user_data)
        self.assertEqual(res.status_code, 200)

    def test_02_get_all_users(self):
        res = self.client.get('/users')
        user = json.loads(res.data)[0]
        self.assertEqual(self.user_data['nric'], user['nric'])
        self.assertEqual(self.user_data['first_name'], user['first_name'])
        self.assertEqual(self.user_data['last_name'], user['last_name'])
        self.assertEqual(self.user_data['password_hash'], user['password_hash'])

    def test_03_get_user(self):
        res = self.client.get(f'/users/{self.user_data["nric"]}')
        user = json.loads(res.data)
        self.assertEqual(self.user_data['nric'], user['nric'])
        self.assertEqual(self.user_data['first_name'], user['first_name'])
        self.assertEqual(self.user_data['last_name'], user['last_name'])
        self.assertEqual(self.user_data['password_hash'], user['password_hash'])

    def test_04_update_user(self):
        self.user_data['first_name'] = 'John'
        self.user_data['last_name'] = 'Lee'
        self.user_data['password'] = 'secret2'
        self.user_data['password_hash'] = '35224d0d3465d74e855f8d69a136e79c744ea35a675d3393360a327cbf6359a2'
        res = self.client.put(f'/users/{self.user_data["nric"]}', data=self.user_data)
        user = json.loads(res.data)
        self.assertEqual(self.user_data['nric'], user['nric'])
        self.assertEqual(self.user_data['first_name'], user['first_name'])
        self.assertEqual(self.user_data['last_name'], user['last_name'])
        self.assertEqual(self.user_data['password_hash'], user['password_hash'])

    def test_05_remove_user(self):
        res = self.client.delete(f'/users/{self.user_data["nric"]}')
        self.assertEqual(200, res.status_code)


if __name__ == "__main__":
    unittest.main(failfast=True)
