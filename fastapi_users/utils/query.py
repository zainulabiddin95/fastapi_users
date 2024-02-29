from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_users.models.user import UserModel


async def save_user(
    *,
    database_session: AsyncSession,
    username: str,
    hashed_password: bytes,
) -> None:
    user_model = UserModel(username=username, hashed_password=hashed_password)
    database_session.add(user_model)


async def get_user(
    *,
    database_session: AsyncSession,
    username: str,
) -> UserModel | None:
    query = select(UserModel).where(UserModel.username == username)

    result = await database_session.execute(query)

    return result.scalar_one_or_none()
