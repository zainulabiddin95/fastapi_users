from pydantic import BaseModel


class AuthData(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
