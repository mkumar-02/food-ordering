from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models.user import User
from app.schemas.menu_item import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse
)
from app.services import menu_service


router = APIRouter(
    tags=["Menu Items"]
)


@router.post(
    "/restaurants/{restaurant_id}/menu-items",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_menu_item(
    restaurant_id: int,
    item_data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("restaurant_owner")
    )
):
    return menu_service.create_menu_item(
        db,
        restaurant_id,
        current_user.id,
        item_data
    )


@router.patch(
    "/menu-items/{item_id}",
    response_model=MenuItemResponse
)
def update_menu_item(
    item_id: int,
    item_data: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("restaurant_owner")
    )
):
    return menu_service.update_menu_item(
        db,
        item_id,
        current_user.id,
        item_data
    )