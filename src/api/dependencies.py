from typing import Annotated
from fastapi import Depends

from src.database import AsyncSession, get_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]