from api.cfg import settings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_db_from_scheema():
    Base.metadata.create_all(engine)


def get_db_session():
    return SessionLocal()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
