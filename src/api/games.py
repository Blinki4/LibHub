from fastapi import APIRouter, status, HTTPException, Response, Depends
from sqlalchemy import select, delete


from src.api.dependencies import SessionDep, SecurityDep
from src.shemas.games import SGameCreate, SGameUpdate, SGameCreateResponse, SGame
from src.models.games import GameOrm
from src.repositories.games import GamesRepository



router = APIRouter()

@router.post(
        '/games',
        dependencies=[SecurityDep],
        status_code=status.HTTP_201_CREATED,
        summary='Добавить игру', 
        tags=['Games 🎮'],
        )
async def create_game(data: SGameCreate) -> SGameCreateResponse:
    game_id = await GamesRepository.add_game(data)
    return {
        'message' : 'Success',
        'game_id': game_id
    }



@router.get(
        '/games',
        dependencies=[SecurityDep],
        summary='Получить список игр',
        tags=['Games 🎮'],
        status_code=status.HTTP_200_OK
        )
async def get_games() -> list[SGame]:
    games = await GamesRepository.find_all()
    return games



@router.put(
        '/games/{game_id}',
        dependencies=[SecurityDep],
        summary='Редактировать игру',
        tags=['Games 🎮'],
        status_code=status.HTTP_200_OK,
        )
async def update_game(game_id: int, data: SGameUpdate, session: SessionDep):
    query = select(GameOrm).where(GameOrm.id == game_id)
    result = await session.execute(query)
    game = result.scalar_one_or_none()

    if not game:
        raise HTTPException(status_code=404) #TODO: Переделать везде на такой вариант

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


@router.get(
        '/games/{game_id}',
        dependencies=[SecurityDep],
        summary='Получить игру по id',
        tags=['Games 🎮']
        )
async def get_game(game_id: int, session: SessionDep, response: Response):
    query = select(GameOrm).where(GameOrm.id == game_id)
    result = await session.execute(query)
    game = result.scalar_one_or_none()
    if not game:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Not Found'}
    return game


@router.delete(
    '/games/{game_id}',
    dependencies=[SecurityDep],
    summary='Удалить игру по id',
    tags=['Games 🎮']
)
async def delete_game(game_id: int, session: SessionDep, response: Response):
    query = delete(GameOrm).where(GameOrm.id == game_id)
    await session.execute(query)
    await session.commit()
    return {'message': 'Success'}