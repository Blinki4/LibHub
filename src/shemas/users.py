from pydantic import BaseModel

from src.models.users import UsersOrm


class SUserLogin(BaseModel):
    username: str
    password: str

class SUserRegister(SUserLogin):
    pass


class SUserRegisterResponse(BaseModel):
    message: str
    user: SUserLogin

class SUserLoginResponse(BaseModel):
    access_token: str