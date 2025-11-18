from src.database import new_session
from src.models.games import GameOrm
from src.shemas.games import SGameCreate, SGame
from sqlalchemy import select


class GamesRepository:
    @classmethod
    async def add_game(cls, data: SGameCreate) -> int:
        async with new_session() as session:
            game_dict = data.model_dump()
            game = GameOrm(**game_dict)
            session.add(game)
            await session.flush()
            await session.commit()
            return game.id


    @classmethod
    async def find_all(cls) -> list[SGame]:
        async with new_session() as session:
            query = select(GameOrm)
            result = await session.execute(query)
            game_models = result.scalars().all()
            game_schemas = [ SGame.model_validate(game_model) for game_model in game_models ]
            return game_schemas