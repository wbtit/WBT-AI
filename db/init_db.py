from sqlmodel import SQLModel, Session, select
from db.session import engine
from models.user_model import User
from models.base import Base
from models.estimation_model import Estimation, Project
from models.drawing_model import Drawing # Ensure all models are imported
from core.security import hash_password
import os
from dotenv import load_dotenv

load_dotenv()

def reset_database():
    # This will drop all tables. Use with caution!
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("Tables dropped.")

def reset_table(model: Base):
    """Drops and recreates a single table."""
    table_name = model.__tablename__
    print(f"Dropping table: {table_name}...")
    model.__table__.drop(engine, checkfirst=True)
    print(f"Creating table: {table_name}...")
    model.__table__.create(engine, checkfirst=False)

def init_db():
    # Create all tables
    # By importing User and Drawing, their metadata is registered
    print("Creating all tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created.")

    # with Session(engine) as session:
    #     # Check if there is already a superuser
    #     admin_email = os.getenv("ADMIN_EMAIL")
    #     if not admin_email:
    #         print("ADMIN_EMAIL not set in environment. Skipping admin user creation.")
    #         return

    #     user = session.exec(select(User).where(User.email == admin_email)).first()
    #     if not user:
    #         print("Creating admin user...")
    #         admin_user = User(
    #             username=os.getenv("ADMIN_USERNAME", "admin"),
    #             email=admin_email,
    #             hashed_password=hash_password(os.getenv("ADMIN_PASSWORD")),
    #             role="ADMIN",
    #             is_active=True
    #         )
    #         session.add(admin_user)
    #         session.commit()
    #         print("Admin user created successfully.")
    
if __name__ == "__main__":
    # To reset the entire database (deletes all data):
    # reset_database()
    # init_db()

    # To reset only the Estimation table:
    reset_table(Estimation)
