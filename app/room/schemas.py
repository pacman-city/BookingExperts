from pydantic import BaseModel


class RoomResponse(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str | None
    services: list[str]
    price: int
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int
