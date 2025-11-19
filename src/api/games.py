from fastapi import APIRouter, status, HTTPException


from src.api.dependencies import SecurityDep
from src.shemas.games import SGameCreate, SGameUpdate, SGameCreateResponse, SGame
from src.repositories.games import GamesRepository



router = APIRouter(
    prefix='/games',
    tags=['Games 🎮']
)


@router.post(
        '',
        dependencies=[SecurityDep],
        status_code=status.HTTP_201_CREATED,
        summary='Добавить игру',
        )
async def create_game(
        data: SGameCreate
) -> SGameCreateResponse:
    game_id = await GamesRepository.add_game(data)
    return {
        'message' : 'Success',
        'game_id': game_id
    }



@router.get(
        '',
        dependencies=[SecurityDep],
        summary='Получить список игр',
        )
async def get_games() -> list[SGame]:
    games = await GamesRepository.find_all()
    return games


@router.put(
        '/{game_id}',
        dependencies=[SecurityDep],
        summary='Редактировать игру',
        )
async def update_game(
        game_id: int, data: SGameUpdate
) -> SGame:
    game = await GamesRepository.update_game(game_id, data)
    if not game:
        raise HTTPException(status_code=404)
    return game


@router.get(
        '/{game_id}',
        dependencies=[SecurityDep],
        summary='Получить игру по id',
        )
async def get_game(
        game_id: int
) -> SGame:
    game = await GamesRepository.find_game(game_id)
    if not game:
        raise HTTPException(status_code=404)
    return game


@router.delete(
    '/{game_id}',
    dependencies=[SecurityDep],
    summary='Удалить игру по id',
)
async def delete_game(
        game_id: int
) -> dict[str, str]:
    await GamesRepository.delete_game(game_id)
    return {'message': 'Success'}