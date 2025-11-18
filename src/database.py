from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


# engine = create_async_engine(
#     "postgresql+asyncpg://admin:SS4MQ9FEEwEUlrkaU4wkftvKSMuDwVtA@dpg-d3rr6nngi27c73faddrg-a.frankfurt-postgres.render.com/lib_hub",
#     )

engine = create_async_engine('sqlite+aiosqlite:///lib_hub.db')


new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


class Model(DeclarativeBase):
    pass


