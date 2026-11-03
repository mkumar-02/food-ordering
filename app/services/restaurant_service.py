from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.exceptions import ResourceNotFound, PermissionDenied


def create_restaurant(
        db: Session,
        restaurant_data: RestaurantCreate,
        owner_id: int
):
    restaurant = Restaurant(
        name=restaurant_data.name,
        cuisine=restaurant_data.cuisine,
        address=restaurant_data.address,
        is_open=restaurant_data.is_open,
        owner_id=owner_id
    )

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return restaurant


def get_restaurants(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Restaurant)
        .order_by(Restaurant.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_restaurant_by_id(db: Session, restaurant_id: int):
    return (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )


def update_restaurant(
        db: Session,
        restaurant: Restaurant,
        restaurant_data: RestaurantUpdate
):
    update_data = restaurant_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(restaurant, field, value)

    db.commit()
    db.refresh(restaurant)

    return restaurant


def get_owned_restaurant(
        db: Session,
        restaurant_id: int,
        owner_id: int
):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if restaurant is None:
        raise ResourceNotFound(
            "Restaurant not found",
            "RESTAURANT_NOT_FOUND"
        )

    if restaurant.owner_id != owner_id:
        raise PermissionDenied(
            "You can manage only your own restaurant",
            "RESTAURANT_ACCESS_DENIED"
        )

    return restaurant
