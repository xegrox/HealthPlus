class AccountAlreadyExistsError(Exception):
    ...


class AccountNotFoundError(Exception):
    ...


class UserNotFoundError(AccountNotFoundError):
    ...


class OrderNotFoundError(Exception):
    ...


class MedicineNotFoundError(Exception):
    ...


class InvalidStaffRoleError(Exception):
    ...
