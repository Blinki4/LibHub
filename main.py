from fastapi import FastAPI, Depends, status, Response

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select, delete
from typing import Annotated

from router import Router
from models.game_model import GameModel, Base
from shemes.game_scheme import GameUpdateSchema, GameCreateShema

app = FastAPI()

engine = create_async_engine(
    "postgresql+asyncpg://admin:SS4MQ9FEEwEUlrkaU4wkftvKSMuDwVtA@dpg-d3rr6nngi27c73faddrg-a.frankfurt-postgres.render.com/lib_hub"
    )


new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.post(
        Router.CREATE_GAME,
        status_code=status.HTTP_201_CREATED,
        summary='Добавить игру', 
        tags=['Games'],
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
    return {'message': 'Success', 
            'game': {
                'id': new_game.id,
                'title': new_game.title,
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
    return [ game for game in data.scalars().all() ]


@app.put(
        '/games/{game_id}',
        summary='Редактировать игру',
        tags=['Games'],
        status_code=status.HTTP_200_OK,
        )
async def update_game(game_id: int, data: GameUpdateSchema, session: SessionDep, response: Response):
    query = select(GameModel).where(GameModel.id == game_id)
    result = await session.execute(query)
    game = result.scalar_one_or_none()

    if not game:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Not Found'}
    

    if data.title:
        game.title = data.title
    if data.description:
        game.description = data.description
    if data.rating:
        game.rating = data.rating
    if data.image_path or data.image_path == '':
        game.image_path = data.image_path

    await session.commit()
    await session.refresh(game)
    return game


@app.get(
        '/games/{game_id}',
        summary='Получить игру по id',
        tags=['Games']
        )
async def get_game(game_id: int, session: SessionDep, response: Response):
    query = select(GameModel).where(GameModel.id == game_id)
    result = await session.execute(query)
    game = result.scalar_one_or_none()
    if not game:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Not Found'}
    return game


@app.delete(
    '/games/{game_id}',
    summary='Удалить игру по id',
    tags=['Games']
)
async def delete_game(game_id: int, session: SessionDep, response: Response):
    query = delete(GameModel).where(GameModel.id == game_id)
    await session.execute(query)
    await session.commit()
    return {'message': 'Success'}



@app.post(
    Router.SETUP_DB,
    summary='Не юзать',
    tags=['Private'],
)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'message': 'Success'}