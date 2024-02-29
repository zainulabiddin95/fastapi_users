from bcrypt import hashpw, gensalt, checkpw


def hash_password(*, password: str) -> bytes:
    return hashpw(password=password.encode(), salt=gensalt())


def check_password(*, hashed_password: bytes, password: str) -> bool:
    return checkpw(password=password.encode(), hashed_password=hashed_password)
