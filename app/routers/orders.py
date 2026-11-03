from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.models.restaurant import Restaurant
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services import order_service
from app.exceptions import ResourceNotFound


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# Customer: Place an order
@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("customer"))
):
    return order_service.create_order(
        db,
        current_user.id,
        order_data
    )


# Customer, owner, admin: View orders with pagination
@router.get("/", response_model=list[OrderResponse])
def list_orders(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return order_service.get_orders(
            db, skip=skip, limit=limit
        )

    if current_user.role == "customer":
        return order_service.get_orders(
            db,
            customer_id=current_user.id,
            skip=skip,
            limit=limit
        )

    if current_user.role == "restaurant_owner":
        restaurant_ids = [
            restaurant.id
            for restaurant in db.query(Restaurant.id).filter(
                Restaurant.owner_id == current_user.id
            ).all()
        ]

        return order_service.get_orders(
            db,
            restaurant_ids=restaurant_ids,
            skip=skip,
            limit=limit
        )

    return []


# Customer, owner, admin: View a particular order
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = order_service.get_order_by_id(db, order_id)

    if order is None:
        raise ResourceNotFound(
            "Order not found",
            "ORDER_NOT_FOUND"
        )

    if current_user.role == "admin":
        return order

    if current_user.role == "customer":
        if order.customer_id != current_user.id:
            from app.exceptions import PermissionDenied
            raise PermissionDenied(
                "You can view only your own orders",
                "ORDER_ACCESS_DENIED"
            )
        return order

    if current_user.role == "restaurant_owner":
        from app.services.restaurant_service import get_owned_restaurant

        get_owned_restaurant(
            db,
            order.restaurant_id,
            current_user.id
        )
        return order

    from app.exceptions import PermissionDenied
    raise PermissionDenied(
        "You do not have permission to view this order",
        "ORDER_ACCESS_DENIED"
    )


# Customer: Cancel own order
@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("customer"))
):
    return order_service.cancel_order(
        db,
        order_id,
        current_user.id
    )

@router.post("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("restaurant_owner")
    )
):
    return order_service.update_order_status(
        db,
        order_id,
        current_user.id,
        status_data.status
    )