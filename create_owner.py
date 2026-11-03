from getpass import getpass

from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import hash_password

db = SessionLocal()

try:
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = getpass("Enter password: ")

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        print("This email is already registered.")
    else:
        owner = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role="restaurant_owner",
            is_active=True
        )

        db.add(owner)
        db.commit()

        print("Restaurant owner created successfully!")

finally:
    db.close()
