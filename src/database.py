import datetime

from sqlalchemy import create_engine, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    sessionmaker,
)

from config import settings

sync_engine = create_engine(settings.db_url, echo=settings.DB_ECHO)
session_factory = sessionmaker(bind=sync_engine)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    # server_default - на уровне БД
    # default - на уровне Python-приложения
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), onupdate=datetime.datetime.now
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__[:-3].lower()
