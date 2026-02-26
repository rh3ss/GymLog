import hashlib


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def compare_passwords(password: str, hashed_password: str) -> bool:
    return hash_password(password=password) == hashed_password
