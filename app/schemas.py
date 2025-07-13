from pydantic import BaseModel, ConfigDict

class HeroCreate(BaseModel):
    name: str

class Hero(BaseModel):
    id: int
    name: str
    intelligence: int
    strength: int
    speed: int
    power: int

    model_config = ConfigDict(from_attributes=True)
