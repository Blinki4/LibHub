from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select

from src.shemas.users import UserRegisterSchema, UserLoginSchema
from src.models.users import UsersModel
from src.api.dependencies import SessionDep
from src.api.config import security, config


router = APIRouter()


@router.post(
        '/register',
        summary='Регистрация',
        tags=['Users 😐']
        )
async def register(creds: UserRegisterSchema, session: SessionDep):
    query = select(UsersModel).where(UsersModel.username == creds.username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(400, 'Имя пользователя занято')
    new_user = UsersModel(
        username = creds.username,
        password = creds.password
    )
    session.add(new_user)
    await session.commit()
    return {
        'message' : 'Success',
        'user': new_user
        }



@router.post(
        '/login',
        summary='Авторизация',
        tags=['Users 😐']
        )
async def login(creds: UserLoginSchema, session: SessionDep, response: Response):
    query = select(UsersModel).where(UsersModel.username == creds.username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, 'Пользователь не найден')
    if user.password != creds.password:
        raise HTTPException(403, 'Неправильный логин или пароль')
    if user.password == creds.password:
        token = security.create_access_token(uid = str(user.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        response.set_cookie('uid', user.id)
    return {'message': 'Success'}