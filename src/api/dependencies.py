from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.api.config import security

SessionDep = Annotated[AsyncSession, Depends(get_session)]
SecurityDep = Depends(security.access_token_required)