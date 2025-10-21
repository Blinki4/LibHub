from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from pydantic import BaseModel
from typing import Annotated


app = FastAPI()

engine = create_async_engine(
    "postgresql+asyncpg://admin:SS4MQ9FEEwEUlrkaU4wkftvKSMuDwVtA@dpg-d3rr6nngi27c73faddrg-a.frankfurt-postgres.render.com/lib_hub"
    )


new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class GameModel(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    rating: Mapped[int]
    image_path: Mapped[str | None]


class GameCreateShema(BaseModel):
    title: str
    description: str
    rating: int
    image_path: str


class GameSchema(GameCreateShema):
    id: int


@app.post('/setup_database')
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {'ok': True}


@app.post('/games')
async def create_game(data: GameCreateShema, session: SessionDep):
    new_game = GameModel(
        title = data.title,
        description = data.description,
        rating = data.rating,
        image_path = data.image_path,
    )
    session.add(new_game)
    await session.commit()
    return {'ok': True, 'game': {
        'title': new_game.title,
        'description': new_game.description,
        'rating': new_game.rating,
        'image_path': new_game.image_path,
    }}