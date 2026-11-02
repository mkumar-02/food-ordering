from fastapi import FastAPI

from app.database import Base, engine

from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem
from app.routers import auth, users
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Ordering API",
    description="API for managing users, restaurants, menus and food orders",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/", tags=["Home"])
def home():
    return {"message": "Welcome to Food Ordering API"}