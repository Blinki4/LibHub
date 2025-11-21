from fastapi import APIRouter, HTTPException, Response


from src.repositories.users import UsersRepository
from src.shemas.users import SUserRegister, SUserLogin, SUserRegisterResponse, SUserLoginResponse
from src.api.config import security, config


router = APIRouter(
    tags=['Users 😐']
)


@router.post(
        '/register',
        summary='Регистрация',
        )
async def register(creds: SUserRegister) -> SUserRegisterResponse:
    try:
        user = await UsersRepository.register(creds)
        return {'message' : 'Success', 'user' : user}
    except ValueError:
        raise HTTPException(400, 'Имя пользователя занято')




@router.post(
        '/login',
        summary='Авторизация',
        )
async def login(creds: SUserLogin, response: Response) -> SUserLoginResponse:
    try:
        user = await UsersRepository.login(creds)
    except ValueError:
        raise HTTPException(404, 'Пользователь не найден')
    except AttributeError:
        raise HTTPException(403, 'Неправильный логин или пароль')
    if user.password == creds.password:
        token = security.create_access_token(uid = str(user.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        response.set_cookie('uid', user.id)
    return {'access_token': token}