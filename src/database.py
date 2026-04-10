from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

sync_engine = create_engine(settings.DB_URL, echo=True)
session_factory = sessionmaker(bind=sync_engine)


class Base(DeclarativeBase):
    pass