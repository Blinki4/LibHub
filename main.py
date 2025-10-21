from fastapi import FastAPI, Depends, status, Response

from router import Router

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, select
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
    image_path: Mapped[str] # TODO обработка


class GameCreateShema(BaseModel):
    title: str
    description: str
    rating: int
    image_path: str


class GameSchema(GameCreateShema):
    id: int


@app.post(
    Router.SETUP_DB,
    summary='Не юзать',
    tags=['Private'],
)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {'ok': True}


@app.post(
        Router.CREATE_GAME,
        summary='Добавить игру', 
        tags=['Games'],
        status_code=status.HTTP_201_CREATED,
        )
async def create_game(data: GameCreateShema, session: SessionDep, response: Response):
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


@app.get(
        Router.GET_GAMES,
        summary='Получить список игр',
        tags=['Games'],
        status_code=status.HTTP_200_OK
        )
async def get_games(session: SessionDep):
    query = select(GameModel)
    data = await session.execute(query)
    return {
        'games' : [
            game for game in data.scalars().all()
        ]
    }

@app.put(
        '/games/{game_id}',
        summary='Редактировать игру',
        tags=['Games'],
        status_code=status.HTTP_200_OK,
        )
async def update_game(game_id: int, data: GameCreateShema, session: SessionDep, response: Response):
    query = select(GameModel).where(GameModel.id == game_id)
    result = await session.execute(query)
    game = result.scalar_one_or_none()

    if not game:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Игра не найдена'}
    
    game.title = data.title
    game.description = data.description
    game.rating = data.rating
    game.image_path = data.image_path

    await session.commit()
    await session.refresh(game)
    return game