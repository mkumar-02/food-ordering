from getpass import getpass

from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import hash_password


def reset_admin_password():
    db = SessionLocal()

    try:
        email = input("Enter admin email: ")
        new_password = getpass("Enter new admin password: ")

        if len(new_password.encode("utf-8")) > 72:
            print("Password must not exceed 72 bytes.")
            return

        admin = db.query(User).filter(
            User.email == email,
            User.role == "admin"
        ).first()

        if not admin:
            print("Admin account not found.")
            return

        admin.hashed_password = hash_password(new_password)

        db.commit()

        print("Admin password reset successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    reset_admin_password()