from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
    RestaurantDetailResponse
)
from app.services import restaurant_service
from app.exceptions import ResourceNotFound

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


@router.get("/", response_model=list[RestaurantResponse])
def list_restaurants(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return restaurant_service.get_restaurants(
        db, skip=skip, limit=limit
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantDetailResponse
)
def get_restaurant(
        restaurant_id: int,
        db: Session = Depends(get_db)
):
    restaurant = restaurant_service.get_restaurant_by_id(
        db, restaurant_id
    )

    if restaurant is None:
        raise ResourceNotFound(
            "Restaurant not found",
            "RESTAURANT_NOT_FOUND"
        )

    return restaurant


@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED
)
def create_restaurant(
        restaurant_data: RestaurantCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(
            require_role("restaurant_owner")
        )
):
    return restaurant_service.create_restaurant(
        db,
        restaurant_data,
        owner_id=current_user.id
    )


@router.patch(
    "/{restaurant_id}",
    response_model=RestaurantResponse
)
def update_restaurant(
        restaurant_id: int,
        restaurant_data: RestaurantUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        restaurant = restaurant_service.get_restaurant_by_id(
            db, restaurant_id
        )

        if restaurant is None:
            raise ResourceNotFound(
                "Restaurant not found",
                "RESTAURANT_NOT_FOUND"
            )

    elif current_user.role == "restaurant_owner":
        restaurant = restaurant_service.get_owned_restaurant(
            db,
            restaurant_id,
            current_user.id
        )

    else:
        from app.exceptions import PermissionDenied
        raise PermissionDenied(
            "Only restaurant owners and admins can update restaurants",
            "RESTAURANT_UPDATE_DENIED"
        )

    return restaurant_service.update_restaurant(
        db,
        restaurant,
        restaurant_data
    )
