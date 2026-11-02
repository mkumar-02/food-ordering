from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    available = Column(Boolean, default=True, nullable=False)

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False
    )

    restaurant = relationship("Restaurant", back_populates="menu_items")
