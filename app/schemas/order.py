
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(ge=1)


class OrderCreate(BaseModel):
    restaurant_id: int
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    total_amount: Decimal
    status: str
    created_at: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: Literal[
        "confirmed",
        "preparing",
        "out_for_delivery",
        "delivered"
    ]
