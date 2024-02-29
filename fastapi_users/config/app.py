import os
from typing import Self


class AppConfig:
    database_url: str
    jwt_secret: str

    def __init__(self: Self) -> None:
        database_url = os.environ.get("DATABASE_URL")
        jwt_secret = os.environ.get("JWT_SECRET")

        if not database_url:
            raise ValueError("error")

        if not jwt_secret:
            raise ValueError("jwt_error")

        self.database_url = database_url
        self.jwt_secret = jwt_secret

    @property
    def async_database_url(self: Self) -> str:
        async_database_url = self.database_url.replace(
            "postgres://",
            "postgresql://",
        ).replace(
            "postgresql://",
            "postgresql+asyncpg://",
        )

        if not async_database_url.startswith("postgresql+asyncpg://"):
            raise ValueError("async_database_url must start with postgresql+asyncpg://")

        return async_database_url


app_config = AppConfig()
