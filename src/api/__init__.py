from fastapi import APIRouter

from src.api.games import router as games_router
from src.api.users import router as users_router


main_router = APIRouter()

main_router.include_router(games_router)
main_router.include_router(users_router)