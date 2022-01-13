from app.database import DatabaseObject


class Medicine(DatabaseObject):
    def __init__(self, medicine_id: str, atc_code: str, name: str, description: str, license_holder: str, quantity: int):
        self._medicine_id = medicine_id
        self._atc_code = atc_code
        self._name = name
        self._description = description
        self._license_holder = license_holder
        self._quantity = quantity

    @property
    def key(self) -> str: return self._medicine_id

    @property
    def medicine_id(self): return self._medicine_id

    @property
    def atc_code(self): return self._atc_code

    @property
    def name(self): return self._name

    @property
    def description(self): return self._description

    @property
    def license_holder(self): return self._license_holder

    def update_quantity(self, quantity): self._quantity = quantity

    @property
    def serializable(self):
        return {
            'medicine_id': self._medicine_id,
            'atc_code': self._atc_code,
            'name': self._name,
            'description': self._description,
            'license_holder': self._license_holder,
            'quantity': self._quantity
        }
