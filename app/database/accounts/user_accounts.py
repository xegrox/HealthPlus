from app.database.database import Database, BasicDatabase
from app.models.account.user import User
from ..exceptions import AccountNotFoundError, AccountAlreadyExistsError
from .utils import hash_sha256, generate_user_id
from ..utils import has_one_of

user_accounts_db = Database('user_accounts')
user_nric_map_db = BasicDatabase('user_nric_map')


def __check_user_exists(account_id):
    with user_accounts_db.open() as accounts:
        if account_id not in accounts:
            raise AccountNotFoundError()


def __read(account_id):
    with user_accounts_db.open() as accounts:
        user = accounts[account_id]
        return user


def __update(account_id, data):
    with user_accounts_db.open() as accounts:
        user = accounts[account_id]
        if val := data.get('nric'):
            with user_nric_map_db.open() as nric_map:
                if val in nric_map:
                    raise AccountAlreadyExistsError()
                # Update nric_map with new nric
                del nric_map[user.nric]
                nric_map[val] = user.get_id()
            user.nric = val
        if val := data.get('first_name'):
            user.first_name = val
        if val := data.get('last_name'):
            user.last_name = val
        if val := data.get('password'):
            user.password_hash = hash_sha256(val)
        accounts.put(user)
        return user


def __delete(account_id):
    with user_accounts_db.open() as accounts:
        with user_nric_map_db.open() as nric_map:
            user = accounts[account_id]
            del nric_map[user.nric]
        accounts.remove(account_id)


def __operation(delegate, account_id=None, nric=None, *args):
    has_one_of(account_id, nric)
    if account_id is not None:
        __check_user_exists(account_id)
        return delegate(account_id, *args)
    if nric is not None:
        with user_nric_map_db.open() as nric_map:
            if nric not in nric_map:
                raise AccountNotFoundError()
            account_id = nric_map[nric]
            __check_user_exists(account_id)
            return delegate(account_id, *args)


def create(nric, first_name, last_name, password):
    with user_accounts_db.open() as accounts:
        with user_nric_map_db.open() as nric_map:
            if nric in nric_map:
                raise AccountAlreadyExistsError()  # Abort if nric already exists
            while (account_id := generate_user_id()) in accounts:
                ...  # Regenerate if generated id already exists
            user = User(
                account_id=account_id,
                nric=nric,
                first_name=first_name,
                last_name=last_name,
                password_hash=hash_sha256(password)
            )
            accounts.put(user)  # Add account
            nric_map[user.nric] = account_id  # Map account_id to nric
            return user


def read(account_id=None, nric=None) -> User:
    return __operation(__read, account_id, nric)


def update(data, account_id=None, nric=None) -> User:
    return __operation(__update, account_id, nric, data)


def delete(account_id=None, nric=None):
    return __operation(__delete, account_id, nric)


def read_all():
    with user_accounts_db.open() as accounts:
        return list(accounts.values())
