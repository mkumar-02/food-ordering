from fastapi import APIRouter, Depends , Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.dependencies import get_current_user, require_role


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    return (
        db.query(User)
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )