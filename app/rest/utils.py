from hashlib import sha256


def hash_sha256(value: str):
    return sha256(value.encode()).hexdigest()