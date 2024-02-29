from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from fastapi_users.config.database import get_database_session
from fastapi_users.schema.auth import AuthData, LoginResponse
from fastapi_users.utils.jwt import encode_jwt, decode_jwt
from fastapi_users.utils.password import hash_password, check_password
from fastapi_users.utils.query import save_user, get_user

auth_router = APIRouter()


@auth_router.post(path="/register")
async def register(
    auth_data: AuthData,
    database_session: AsyncSession = Depends(get_database_session),
) -> Response:
    user = await get_user(
        database_session=database_session,
        username=auth_data.username,
    )

    if user:
        return Response(status_code=403)

    hashed_password = hash_password(password=auth_data.password)

    await save_user(
        database_session=database_session,
        username=auth_data.username,
        hashed_password=hashed_password,
    )

    await database_session.commit()

    return Response(status_code=201)


@auth_router.post(path="/login", response_model=LoginResponse)
async def login(
    auth_data: AuthData,
    database_session: AsyncSession = Depends(get_database_session),
) -> Response | LoginResponse:
    user = await get_user(
        database_session=database_session,
        username=auth_data.username,
    )

    if not user:
        return Response(status_code=403)

    if not check_password(
        hashed_password=user.hashed_password,
        password=auth_data.password,
    ):
        return Response(status_code=403)

    jwt = encode_jwt(username=user.username)

    return LoginResponse(token=jwt)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@auth_router.get(path="/protected")
async def protected(
    token: Annotated[str, Depends(oauth2_scheme)],
    database_session: AsyncSession = Depends(get_database_session),
) -> Response:

    username = decode_jwt(jwt_token=token)
    if not username:
        return Response(status_code=403)

    user = await get_user(database_session=database_session, username=username)
    if not user:
        return Response(status_code=403)

    return Response(status_code=200, content=f"Hello, {user.username}")
