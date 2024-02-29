from jose import JWTError
from jose.jwt import encode, decode

from fastapi_users.config.app import app_config


def encode_jwt(*, username: str) -> str:
    return encode(
        claims={"username": username},
        key=app_config.jwt_secret,
        algorithm="HS256",
    )


def decode_jwt(*, jwt_token: str) -> str | None:
    try:
        decoded = decode(
            token=jwt_token,
            key=app_config.jwt_secret,
            algorithms=["HS256"],
        )
    except JWTError:
        return None

    return decoded["username"]
