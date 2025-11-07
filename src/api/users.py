from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select

from src.shemas.users import UserRegisterSchema, UserLoginSchema
from src.models.users import UsersModel
from src.api.dependencies import SessionDep


router = APIRouter()


@router.post(
        '/register',
        summary='Регистрация',
        tags=['Users 😐']
        )
async def register(creds: UserRegisterSchema, session: SessionDep):
    # Проверить нет ли уже такого пользователя в бд
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
    ...