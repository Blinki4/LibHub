from sqlalchemy import select


from src.database import new_session
from src.models.users import UsersOrm
from src.shemas.users import SUserRegister, SUserLogin


class UsersRepository:

    @classmethod
    async def register(cls, creds: SUserRegister) -> SUserLogin:
        async with new_session() as session:
            query = select(UsersOrm).where(UsersOrm.username == creds.username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                raise ValueError('User already exist')
            new_user = UsersOrm(
                username=creds.username,
                password=creds.password
            )
            session.add(new_user)
            await session.commit()
            return new_user

    @classmethod
    async def login(cls, creds: SUserLogin) -> SUserLogin:
        async with new_session() as session:
            query = select(UsersOrm).where(UsersOrm.username == creds.username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                raise ValueError('Пользователь не найден')
            if user.password != creds.password:
                raise AttributeError('Неправильный логин или пароль')
            return user