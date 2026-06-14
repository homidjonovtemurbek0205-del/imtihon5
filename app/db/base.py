from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

engine = create_engine(settings.DB_URL)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine)