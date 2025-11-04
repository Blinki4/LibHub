from fastapi import APIRouter

from src.api.games import router as games_router


main_router = APIRouter()

main_router.include_router(games_router)