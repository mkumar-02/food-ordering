from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    available: bool = True


class MenuItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    price: Decimal | None = Field(
        default=None, gt=0, max_digits=10, decimal_places=2
    )
    available: bool | None = None


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    available: bool
    restaurant_id: int

    model_config = ConfigDict(from_attributes=True)
