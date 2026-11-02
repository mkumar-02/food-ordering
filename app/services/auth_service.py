from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def register_user(db: Session, user_data: UserCreate):

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise ValueError("Email is already registered")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role="customer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }