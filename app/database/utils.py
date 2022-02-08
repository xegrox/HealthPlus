from app.database.exceptions import UserNotFoundError, StaffNotFoundError


def has_one_of(*args):
    if all(v is None for v in args):
        raise TypeError('Expected one of the arguments to be filled')


def check_user_exists(user_id):
    from app.database.accounts.user_accounts import user_accounts_db
    with user_accounts_db.open() as user_accounts:
        if user_id not in user_accounts:
            raise UserNotFoundError()


def check_staff_exists(staff_id, role):
    from app.database.accounts.staff_accounts import staff_accounts_db
    with staff_accounts_db.open() as staff_accounts:
        if staff_id not in staff_accounts or staff_accounts[staff_id].role != role:
            raise StaffNotFoundError()
