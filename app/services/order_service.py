from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate
from app.exceptions import ResourceNotFound, BusinessRuleViolation


def create_order(
    db: Session,
    customer_id: int,
    order_data: OrderCreate
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == order_data.restaurant_id)
        .first()
    )

    if restaurant is None:
        raise ResourceNotFound(
            "Restaurant not found",
            "RESTAURANT_NOT_FOUND"
        )

    if not restaurant.is_open:
        raise BusinessRuleViolation(
            "Restaurant is currently closed",
            "RESTAURANT_CLOSED"
        )

    item_ids = [item.menu_item_id for item in order_data.items]

    if len(item_ids) != len(set(item_ids)):
        raise BusinessRuleViolation(
            "Duplicate menu items are not allowed in one order",
            "DUPLICATE_ORDER_ITEMS"
        )

    order_items = []
    total_amount = Decimal("0.00")

    for requested_item in order_data.items:

        menu_item = (
            db.query(MenuItem)
            .filter(
                MenuItem.id == requested_item.menu_item_id,
                MenuItem.restaurant_id == restaurant.id
            )
            .first()
        )

        if menu_item is None:
            raise BusinessRuleViolation(
                "Menu item does not belong to this restaurant",
                "INVALID_MENU_ITEM"
            )

        if not menu_item.available:
            raise BusinessRuleViolation(
                f"{menu_item.name} is currently unavailable",
                "MENU_ITEM_UNAVAILABLE"
            )

        quantity = requested_item.quantity

        unit_price = Decimal(str(menu_item.price))

        order_item = OrderItem(
            menu_item_id=menu_item.id,
            quantity=quantity,
            unit_price=unit_price
        )

        order_items.append(order_item)

        total_amount += unit_price * quantity

    new_order = Order(
        customer_id=customer_id,
        restaurant_id=restaurant.id,
        total_amount=total_amount,
        status="placed",
        items=order_items
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

def get_order_by_id(db: Session, order_id: int):
    return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )


def get_orders(
    db: Session,
    customer_id: int | None = None,
    restaurant_ids: list[int] | None = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(Order)

    if customer_id is not None:
        query = query.filter(Order.customer_id == customer_id)

    if restaurant_ids is not None:
        query = query.filter(Order.restaurant_id.in_(restaurant_ids))

    return (
        query.order_by(Order.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def cancel_order(
    db: Session,
    order_id: int,
    customer_id: int
):
    order = get_order_by_id(db, order_id)

    if order is None:
        raise ResourceNotFound(
            "Order not found",
            "ORDER_NOT_FOUND"
        )

    if order.customer_id != customer_id:
        from app.exceptions import PermissionDenied
        raise PermissionDenied(
            "You can cancel only your own orders",
            "ORDER_ACCESS_DENIED"
        )

    if order.status not in ("placed", "confirmed"):
        raise BusinessRuleViolation(
            "Only placed or confirmed orders can be cancelled",
            "ORDER_NOT_CANCELLABLE"
        )

    order.status = "cancelled"

    db.commit()
    db.refresh(order)

    return order

def update_order_status(
    db: Session,
    order_id: int,
    owner_id: int,
    new_status: str
):
    order = get_order_by_id(db, order_id)

    if order is None:
        raise ResourceNotFound(
            "Order not found",
            "ORDER_NOT_FOUND"
        )

    from app.services.restaurant_service import get_owned_restaurant

    get_owned_restaurant(
        db,
        order.restaurant_id,
        owner_id
    )

    status_flow = {
        "placed": "confirmed",
        "confirmed": "preparing",
        "preparing": "out_for_delivery",
        "out_for_delivery": "delivered"
    }

    expected_status = status_flow.get(order.status)

    if expected_status != new_status:
        raise BusinessRuleViolation(
            f"Invalid status transition. Next status must be {expected_status}",
            "INVALID_ORDER_STATUS_TRANSITION"
        )

    order.status = new_status

    db.commit()
    db.refresh(order)

    return order