from src.database import new_session
from src.models.games import GameOrm
from src.shemas.games import SGameCreate, SGame, SGameUpdate
from sqlalchemy import select, delete


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


    @classmethod
    async def update_game(cls, game_id: int, data: SGameUpdate) -> SGame | None:
        async with new_session() as session:
            query = select(GameOrm).where(GameOrm.id == game_id)
            result = await session.execute(query)
            game_model = result.scalar_one_or_none()

            if not game_model:
                return None

            if data.title:
                game_model.title = data.title
            if data.description:
                game_model.description = data.description
            if data.rating:
                game_model.rating = data.rating
            if data.image_path or data.image_path == '':
                game_model.image_path = data.image_path

            await session.commit()
            await session.refresh(game_model)
            return game_model


    @classmethod
    async def find_game(cls, game_id: int) -> SGame | None:
        async with new_session() as session:
            query = select(GameOrm).where(GameOrm.id == game_id)
            result = await session.execute(query)
            game_model = result.scalar_one_or_none()

            if not game_model:
                return None

            return game_model


    @classmethod
    async def delete_game(cls, game_id: int) -> None:
        async with new_session() as session:
            query = delete(GameOrm).where(GameOrm.id == game_id)
            await session.execute(query)
            await session.commit()
