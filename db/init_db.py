from sqlmodel import SQLModel, Session, select
from db.session import engine
from models.user_model import User
from core.security import hash_password
import os

def init_db():
    # Create all tables
    SQLModel.metadata.create_all(engine)

    # Create a first superuser if the database is empty
    with Session(engine) as session:
        user = session.exec(select(User)).first()
        if not user:
            print("Database is empty. Creating first superuser...")
            admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
            admin_password = os.getenv("ADMIN_PASSWORD", "changeme")
            
            admin_user = User(
                email=admin_email,
                username="admin",
                hashed_password=hash_password(admin_password),
                role="ADMIN",
                is_active=True
            )
            session.add(admin_user)
            session.commit()
            print(f"Superuser '{admin_email}' created with a default password.")

if __name__ == "__main__":
    init_db()
