from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate
from app.services.restaurant_service import get_owned_restaurant
from app.exceptions import ResourceNotFound

def create_menu_item(
        db: Session,
        restaurant_id: int,
        owner_id: int,
        item_data: MenuItemCreate
):
    restaurant = get_owned_restaurant(
        db, restaurant_id, owner_id
    )

    menu_item = MenuItem(
        name=item_data.name,
        description=item_data.description,
        price=item_data.price,
        available=item_data.available,
        restaurant_id=restaurant.id
    )

    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)

    return menu_item


def get_menu_item_by_id(db: Session, item_id: int):
    return (
        db.query(MenuItem)
        .filter(MenuItem.id == item_id)
        .first()
    )


def update_menu_item(
        db: Session,
        item_id: int,
        owner_id: int,
        item_data: MenuItemUpdate
):
    menu_item = get_menu_item_by_id(db, item_id)

    if menu_item is None:
        raise ResourceNotFound(
            "Menu item not found",
            "MENU_ITEM_NOT_FOUND"
        )

    get_owned_restaurant(
        db,
        menu_item.restaurant_id,
        owner_id
    )

    update_data = item_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if value is not None or field == "description":
            setattr(menu_item, field, value)

    db.commit()
    db.refresh(menu_item)

    return menu_item
