from sqlalchemy import (
    Column, Integer, String, ForeignKey, Numeric, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False
    )

    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(30), default="placed", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("User", backref="orders")
    restaurant = relationship("Restaurant", backref="orders")

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(
        Integer,
        ForeignKey("menu_items.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")
