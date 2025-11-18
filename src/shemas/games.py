from pydantic import BaseModel, ConfigDict


class SGameUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    description: str | None = None
    rating: int | None = None
    image_path: str | None = None


class SGameCreate(SGameUpdate):
    title: str


class SGame(SGameCreate):
    id: int

class SGameCreateResponse(BaseModel):
    message: str
    game_id: int