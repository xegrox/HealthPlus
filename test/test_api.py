import json
import os
from app import app
import unittest

from app.database.accounts import staff_accounts


class TestUserAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()
        cls.user_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'nric': 'T0123456A',
            'password': 'secret'
        }

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('user_accounts')
        os.remove('user_nric_map')

    def test_01_signup(self):
        res = self.client.post('/account', data=self.user_data)
        self.assertEqual(200, res.status_code)

    def test_02_login(self):
        res = self.client.post('session', data={
            'nric': self.user_data['nric'],
            'password': self.user_data['password']
        })
        self.assertEqual(200, res.status_code)

    def test_03_get_info(self):
        res = self.client.get('/account')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data)
        self.assertCountEqual(data.keys(), ['nric', 'first_name', 'last_name'])
        self.assertEqual(data['nric'], self.user_data['nric'])
        self.assertEqual(data['first_name'], self.user_data['first_name'])
        self.assertEqual(data['last_name'], self.user_data['last_name'])

    def test_04_update_info(self):
        old_nric = self.user_data['nric']
        self.user_data['nric'] = 'T0123456B'
        self.user_data['first_name'] = 'Tom'
        self.user_data['last_name'] = 'Lee'
        self.user_data['password'] = 'secret2'
        res = self.client.put('/account', data=self.user_data)
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data)
        self.assertCountEqual(data.keys(), ['nric', 'first_name', 'last_name'])
        self.assertEqual(data['nric'], old_nric)  # User cannot change nric
        self.assertEqual(data['first_name'], self.user_data['first_name'])
        self.assertEqual(data['last_name'], self.user_data['last_name'])
        self.user_data['nric'] = old_nric

    def test_05_logout(self):
        res = self.client.delete('session')
        self.assertEqual(200, res.status_code)

    def test_06_delete_account(self):
        self.test_02_login()
        res = self.client.delete('/account', data={'password': self.user_data['password']})
        self.assertEqual(200, res.status_code)
        res = self.client.post('session', data=self.user_data)
        self.assertEqual(401, res.status_code)


class TestStaffAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()
        staff_data = {
            'staff_id': '123456789A',
            'role': 'doctor',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': 'secret'
        }
        staff_accounts.create(**staff_data)
        cls.staff_data = staff_data

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('staff_accounts')
        os.remove('staff_id_map')

    def test_01_login(self):
        res = self.client.post('session', data={
            'staff_id': self.staff_data['staff_id'],
            'password': self.staff_data['password']
        })
        self.assertEqual(200, res.status_code)

    def test_02_get_info(self):
        res = self.client.get('/account')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data)
        self.assertCountEqual(data.keys(), ['staff_id', 'role', 'first_name', 'last_name'])
        self.assertEqual(data['staff_id'], self.staff_data['staff_id'])
        self.assertEqual(data['role'], self.staff_data['role'])
        self.assertEqual(data['first_name'], self.staff_data['first_name'])
        self.assertEqual(data['last_name'], self.staff_data['last_name'])

    def test_03_update_info(self):
        res = self.client.put('/account', data={
            'staff_id': '123456789B',
            'role': 'pharmacist',
            'first_name': 'Tom',
            'last_name': 'Lee',
            'password': 'secret2'
        })
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data)
        self.assertCountEqual(data.keys(), ['staff_id', 'role', 'first_name', 'last_name'])
        # Staff can only change password
        self.assertEqual(data['staff_id'], self.staff_data['staff_id'])
        self.assertEqual(data['role'], self.staff_data['role'])
        self.assertEqual(data['first_name'], self.staff_data['first_name'])
        self.assertEqual(data['last_name'], self.staff_data['last_name'])

    def test_04_logout(self):
        res = self.client.delete('session')
        self.assertEqual(200, res.status_code)


if __name__ == "__main__":
    unittest.main(failfast=True)
