from uuid import uuid4

from app.database import Database
from app.database.exceptions import MedicineNotFoundError
from app.models.medicine import Medicine

medicine_inventory_db = Database('medicine_inventory')


def __get_medicine(inv, medicine_id) -> Medicine:
    try:
        return inv[medicine_id]
    except KeyError:
        raise MedicineNotFoundError()


def create(atc_code, name, description, license_holder, quantity, price):
    medicine = Medicine(uuid4().hex, atc_code, name, description, license_holder, quantity, price)
    with medicine_inventory_db.open() as inv:
        inv.put(medicine)
        return medicine


def read(medicine_id):
    with medicine_inventory_db.open() as inv:
        return __get_medicine(inv, medicine_id)


def update(medicine_id, quantity):
    with medicine_inventory_db.open() as inv:
        medicine = __get_medicine(inv, medicine_id)
        medicine.update_quantity(quantity)
        inv.put(medicine)
        return medicine


def delete(medicine_id):
    with medicine_inventory_db.open() as inv:
        try:
            del inv[medicine_id]
        except KeyError:
            raise MedicineNotFoundError()


def read_all():
    with medicine_inventory_db.open() as inv:
        return list(inv.values())
