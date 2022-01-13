from app.database.database import Database, BasicDatabase
from app.models.account.staff import Staff, StaffRole
from app.database.exceptions import AccountNotFoundError, AccountAlreadyExistsError, InvalidStaffRoleError
from .utils import has_one_of, hash_sha256, generate_staff_id

staff_accounts_db = Database('staff_accounts')
staff_id_map_db = BasicDatabase('staff_id_map')


def __check_staff_exists(account_id):
    with staff_accounts_db.open() as accounts:
        if account_id not in accounts:
            raise AccountNotFoundError()


def __read(account_id):
    with staff_accounts_db.open() as accounts:
        staff = accounts[account_id]
        return staff


def __update(account_id, data):
    with staff_accounts_db.open() as accounts:
        staff = accounts[account_id]
        if val := data.get('staff_id'):
            with staff_id_map_db.open() as sid_map:
                if val in sid_map:
                    raise AccountAlreadyExistsError()
                # Update staff_id_map with new staff id
                del sid_map[staff.staff_id]
                sid_map[val] = staff.get_id()
            staff.staff_id = val
        if val := data.get('role'):
            try:
                staff.role = StaffRole(val)
            except ValueError:
                raise InvalidStaffRoleError()
        if val := data.get('first_name'):
            staff.first_name = val
        if val := data.get('last_name'):
            staff.last_name = val
        if val := data.get('password'):
            staff.password_hash = hash_sha256(val)
        accounts.put(staff)
        return staff


def __delete(account_id):
    with staff_accounts_db.open() as accounts:
        with staff_id_map_db.open() as sid_map:
            staff = accounts[account_id]
            del sid_map[staff.staff_id]
        accounts.remove(account_id)


def __operation(delegate, account_id=None, staff_id=None, *args):
    has_one_of(account_id, staff_id)
    if account_id is not None:
        __check_staff_exists(account_id)
        return delegate(account_id, *args)
    if staff_id is not None:
        with staff_id_map_db.open() as sid_map:
            if staff_id not in sid_map:
                raise AccountNotFoundError()
            account_id = sid_map[staff_id]
            __check_staff_exists(account_id)
            return delegate(account_id, *args)


def create(role, staff_id, first_name, last_name, password):
    with staff_accounts_db.open() as accounts:
        with staff_id_map_db.open() as sid_map:
            if staff_id in sid_map:
                raise AccountAlreadyExistsError()  # Abort if staff id already exists
            while (account_id := generate_staff_id()) in accounts:
                ...  # Regenerate if generated id already exists
            try:
                role = StaffRole(role)
            except ValueError:
                raise InvalidStaffRoleError()
            staff = Staff(
                role=role,
                account_id=account_id,
                staff_id=staff_id,
                first_name=first_name,
                last_name=last_name,
                password_hash=hash_sha256(password)
            )
            accounts.put(staff)  # Add account
            sid_map[staff.staff_id] = account_id  # Map account_id to staff id
            return staff


def read(account_id=None, staff_id=None) -> Staff:
    return __operation(__read, account_id, staff_id)


def update(data, account_id=None, staff_id=None) -> Staff:
    return __operation(__update, account_id, staff_id, data)


def delete(account_id=None, staff_id=None):
    return __operation(__delete, account_id, staff_id)


def read_all():
    with staff_accounts_db.open() as accounts:
        return list(accounts.values())
