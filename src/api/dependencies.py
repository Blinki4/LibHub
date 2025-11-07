from typing import Annotated
from fastapi import Depends

from src.database import AsyncSession, get_session
from src.api.config import security

SessionDep = Annotated[AsyncSession, Depends(get_session)]
SecurityDep = Depends(security.access_token_required)