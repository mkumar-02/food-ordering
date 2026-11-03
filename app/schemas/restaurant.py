from pydantic import BaseModel, ConfigDict, Field
from app.schemas.menu_item import MenuItemResponse


class RestaurantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    cuisine: str = Field(min_length=2, max_length=100)
    address: str = Field(min_length=5, max_length=255)
    is_open: bool = True


class RestaurantUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    cuisine: str | None = Field(default=None, min_length=2, max_length=100)
    address: str | None = Field(default=None, min_length=5, max_length=255)
    is_open: bool | None = None


class RestaurantResponse(BaseModel):
    id: int
    name: str
    cuisine: str
    address: str
    is_open: bool
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class RestaurantDetailResponse(RestaurantResponse):
    menu_items: list[MenuItemResponse] = []
