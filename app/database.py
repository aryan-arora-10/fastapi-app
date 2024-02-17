# to create the engine for SQLalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# dialect+driver://username:password@host:port/database_name
SQLALCHEMY_DATABSE_URL =f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

# engine = create_engine(SQLALCHEMY_DATABSE_URL)


try:
    engine = create_engine(SQLALCHEMY_DATABSE_URL)
    print("Connection established successfully from SQL alchemy")
except:
    print("Sorry session could not be established")


SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()