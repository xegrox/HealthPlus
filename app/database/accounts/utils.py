import random
import string
from hashlib import sha256


def has_one_of(*args):
    if all(v is None for v in args):
        raise ValueError('Expected one of the arguments to be filled')


def __generate_id():
    rand_num = random.randrange(0, 99999)
    rand_letter = random.choice(string.ascii_uppercase)
    return '%03d' % rand_num + rand_letter


def generate_user_id():
    return 'U' + __generate_id()


def generate_staff_id():
    return 'S' + __generate_id()


def hash_sha256(value: str):
    return sha256(value.encode()).hexdigest()
