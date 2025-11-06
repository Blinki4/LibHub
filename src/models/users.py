from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class UsersModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]