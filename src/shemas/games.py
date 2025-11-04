from typing import Union
from pydantic import BaseModel


class GameUpdateSchema(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None
    rating: Union[int, None] = None
    image_path: Union[str, None] = None


class GameCreateShema(GameUpdateSchema):
    title: str
    

class GameSchema(GameCreateShema):
    id: int
