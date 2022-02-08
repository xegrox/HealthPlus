import datetime
import json
import os
from app import app
import unittest

from app.database.accounts import staff_accounts, user_accounts
from app.database.pharmacist import medicine_inventory


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
        self.user_data['first_name'] = 'Tom'
        self.user_data['last_name'] = 'Lee'
        res = self.client.put('/account', data={
            'nric': 'T0123456B',
            'first_name': self.user_data['first_name'],
            'last_name': self.user_data['last_name'],
            'current_password': self.user_data['password'],
            'new_password': 'secret2'
        })
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data)
        self.assertCountEqual(data.keys(), ['nric', 'first_name', 'last_name'])
        self.assertEqual(data['nric'], self.user_data['nric'])  # User cannot change nric
        self.assertEqual(data['first_name'], self.user_data['first_name'])
        self.assertEqual(data['last_name'], self.user_data['last_name'])
        self.user_data['password'] = 'secret2'

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


class TestPharmacistMedicineInventory(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        staff_data = {
            'role': 'pharmacist',
            'staff_id': 'test',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': '123'
        }
        cls.staff_data = staff_data
        staff_accounts.create(**staff_data)
        cls.client = app.test_client()
        cls.medicine_data = {
            'atc_code': 'L01XE45',
            'name': 'Amlodipine',
            'description': 'calcium channel blocker medication used to treat high blood pressure and coronary artery disease',
            'license_holder': 'Specialised Therapeutics Asia Pte. Ltd.',
            'quantity': 701
        }

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('staff_accounts')
        os.remove('staff_id_map')
        os.remove('medicine_inventory')

    def __login(self):
        res = self.client.post('/session', data=self.staff_data)
        self.assertEqual(res.status_code, 200)

    def test_01_add_medicine(self):
        self.__login()
        res = self.client.post('/medicine', data=self.medicine_data)
        self.assertEqual(res.status_code, 200)
        self.medicine_data['medicine_id'] = json.loads(res.data)['medicine_id']

    def test_02_get_all_medicine(self):
        self.__login()
        res = self.client.get('/medicine')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 1)
        medicine_data = data[0]
        self.assertEqual(medicine_data['medicine_id'], self.medicine_data['medicine_id'])
        self.assertEqual(medicine_data['atc_code'], self.medicine_data['atc_code'])
        self.assertEqual(medicine_data['name'], self.medicine_data['name'])
        self.assertEqual(medicine_data['description'], self.medicine_data['description'])
        self.assertEqual(medicine_data['license_holder'], self.medicine_data['license_holder'])
        self.assertEqual(medicine_data['quantity'], self.medicine_data['quantity'])

    def test_03_get_medicine(self):
        self.__login()
        res = self.client.get(f'/medicine/{self.medicine_data["medicine_id"]}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['medicine_id'], self.medicine_data['medicine_id'])
        self.assertEqual(data['atc_code'], self.medicine_data['atc_code'])
        self.assertEqual(data['name'], self.medicine_data['name'])
        self.assertEqual(data['description'], self.medicine_data['description'])
        self.assertEqual(data['license_holder'], self.medicine_data['license_holder'])
        self.assertEqual(data['quantity'], self.medicine_data['quantity'])

    def test_04_update_medicine(self):
        new_quantity = 703
        self.__login()
        res = self.client.put(f'/medicine/{self.medicine_data["medicine_id"]}', data={'quantity': new_quantity})
        self.medicine_data['quantity'] = new_quantity
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['medicine_id'], self.medicine_data['medicine_id'])
        self.assertEqual(data['atc_code'], self.medicine_data['atc_code'])
        self.assertEqual(data['name'], self.medicine_data['name'])
        self.assertEqual(data['description'], self.medicine_data['description'])
        self.assertEqual(data['license_holder'], self.medicine_data['license_holder'])
        self.assertEqual(data['quantity'], self.medicine_data['quantity'])

    def test_05_delete_medicine(self):
        self.__login()
        res = self.client.delete(f'/medicine/{self.medicine_data["medicine_id"]}')
        self.assertEqual(res.status_code, 200)


class TestUserMedicineOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        user_data = {
            'nric': 'test',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': '123'
        }
        user_accounts.create(**user_data)
        cls.user_data = user_data

        medicine_data_1 = {
            'atc_code': 'L01XE45',
            'name': 'Amlodipine',
            'description': 'calcium channel blocker medication used to treat high blood pressure and coronary artery disease',
            'license_holder': 'Specialised Therapeutics Asia Pte. Ltd.',
            'quantity': 701
        }

        medicine_data_2 = {
            'atc_code': 'C10AA08',
            'name': 'Aspirin',
            'description': 'medication used to reduce pain, fever, or inflammation',
            'license_holder': 'DKSH Singapore Pte. Ltd.',
            'quantity': 980
        }

        medicine_1 = medicine_inventory.create(**medicine_data_1)
        medicine_2 = medicine_inventory.create(**medicine_data_2)
        cls.medicine_1 = medicine_1
        cls.medicine_2 = medicine_2

        order_request_data = {
            'method': 'delivery',
            'quantities': {
                medicine_1.medicine_id: 5,
                medicine_2.medicine_id: 10
            }
        }
        cls.order_request_data = order_request_data
        cls.client = app.test_client()
        cls.order_data = {}

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('user_accounts')
        os.remove('user_nric_map')
        os.remove('medicine_inventory')
        os.remove('user_medicine_orders')

    def __login(self):
        res = self.client.post('/session', data=self.user_data)
        self.assertEqual(res.status_code, 200)

    def test_01_add_order(self):
        self.__login()
        res = self.client.post('/medicine_order', data=json.dumps(self.order_request_data), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['method'], 'delivery')
        self.assertEqual(data['status'], 'pending')
        medicine_1_data = data['quantities'][0]
        self.assertDictEqual(medicine_1_data, {
            'medicine_id': self.medicine_1.medicine_id,
            'name': self.medicine_1.name,
            'description': self.medicine_1.description,
            'atc_code': self.medicine_1.atc_code,
            'quantity': self.order_request_data['quantities'][self.medicine_1.medicine_id]
        })
        medicine_2_data = data['quantities'][1]
        self.assertDictEqual(medicine_2_data, {
            'medicine_id': self.medicine_2.medicine_id,
            'name': self.medicine_2.name,
            'description': self.medicine_2.description,
            'atc_code': self.medicine_2.atc_code,
            'quantity': self.order_request_data['quantities'][self.medicine_2.medicine_id]
        })
        today = datetime.date.today()
        self.assertDictEqual(data['date'], {
            'day': today.day,
            'month': today.month,
            'year': today.year
        })
        self.order_data.update(data)

    def test_02_get_all_orders(self):
        self.__login()
        res = self.client.get('/medicine_order')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data[0]['order_id'], self.order_data['order_id'])
        self.assertEqual(data[0]['method'], self.order_data['method'])
        self.assertListEqual(data[0]['quantities'], self.order_data['quantities'])
        self.assertDictEqual(data[0]['date'], self.order_data['date'])
        self.assertEqual(data[0]['status'], 'pending')
        self.order_data.update(data[0])

    def test_03_get_order(self):
        self.__login()
        res = self.client.get(f'/medicine_order/{self.order_data["order_id"]}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['order_id'], self.order_data['order_id'])
        self.assertEqual(data['method'], self.order_data['method'])
        self.assertListEqual(data['quantities'], self.order_data['quantities'])
        self.assertDictEqual(data['date'], self.order_data['date'])
        self.assertEqual(data['status'], self.order_data['status'])

    def test_04_delete_order(self):
        self.__login()
        res = self.client.delete(f'/medicine_order/{self.order_data["order_id"]}')
        self.assertEqual(res.status_code, 200)


class TestUserAvailableMedicine(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        user_data = {
            'nric': 'test',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': '123'
        }
        user_accounts.create(**user_data)
        cls.user_data = user_data

        medicine_data = {
            'atc_code': 'L01XE45',
            'name': 'Amlodipine',
            'description': 'calcium channel blocker medication used to treat high blood pressure and coronary artery disease',
            'license_holder': 'Specialised Therapeutics Asia Pte. Ltd.',
            'quantity': 701
        }
        cls.medicine = medicine_inventory.create(**medicine_data)
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('user_accounts')
        os.remove('user_nric_map')
        os.remove('medicine_inventory')

    def __login(self):
        res = self.client.post('/session', data=self.user_data)
        self.assertEqual(res.status_code, 200)

    def test_01_get_all_medicine(self):
        self.__login()
        res = self.client.get('/available_medicine')
        data = json.loads(res.data)
        medicine_data = data[0]
        self.assertEqual(res.status_code, 200)
        self.assertEqual(medicine_data['medicine_id'], self.medicine.medicine_id)
        self.assertEqual(medicine_data['name'], self.medicine.name)
        self.assertEqual(medicine_data['description'], self.medicine.description)
        self.assertEqual(medicine_data['atc_code'], self.medicine.atc_code)


class TestUserAppointments(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()
        cls.doctor = staff_accounts.create('doctor', 'test_doctor', 'John', 'Smith', '')
        user_accounts.create('test_user', '', '', '123')
        cls.appointment_data = {}

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('user_accounts')
        os.remove('user_nric_map')
        os.remove('staff_accounts')
        os.remove('staff_id_map')
        os.remove('appointments')
        os.remove('appointments_user_map')
        os.remove('appointments_doctor_map')

    def __login(self):
        res = self.client.post('/session', data={'nric': 'test_user', 'password': 123})
        self.assertEqual(res.status_code, 200)

    def test_01_add_appointment(self):
        self.__login()
        res = self.client.post('/appointment', data={
            'doctor_id': self.doctor.get_id(),
            'datetime': '2020-02-08T09:30',
            'condition': 'test condition',
            'description': 'test description'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        assert data.items() >= {
            'status': 'Booked',
            'doctor_name': 'Dr John Smith',
            'datetime': '2020-02-08T09:30:00',
            'condition': 'test condition',
            'description': 'test description'
        }.items()
        self.appointment_data.update(data)

    def test_02_get_all_appointments(self):
        self.__login()
        res = self.client.get(f'/appointment')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertDictEqual(data[0], self.appointment_data)

    def test_03_get_appointment(self):
        self.__login()
        res = self.client.get(f'/appointment/{self.appointment_data["appointment_id"]}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertDictEqual(data, self.appointment_data)

    def test_04_delete_appointment(self):
        self.__login()
        res = self.client.delete(f'/appointment/{self.appointment_data["appointment_id"]}')
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main(failfast=True)
