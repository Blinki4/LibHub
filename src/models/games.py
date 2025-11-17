from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class GameModel(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    rating: Mapped[int | None]
    image_path: Mapped[str | None]
    #user_id: Mapped[int | None] #TODO: Внешний ключ