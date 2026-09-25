from pydantic import BaseModel, ConfigDict

class RoomCreateSchema(BaseModel):

    title: str
    description: str
    quantity: int
    price: int

class RoomReadSchema(BaseModel):

    id: int
    title: str
    description: str | None
    quantity: int
    price: int

    model_config = ConfigDict(from_attributes=True)