from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    cuisine = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    is_open = Column(Boolean, default=True, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", backref="restaurants")
    menu_items = relationship(
        "MenuItem",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )
