import datetime

from sqlalchemy import create_engine, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, declared_attr

from config import settings

sync_engine = create_engine(settings.DB_URL, echo=True)
session_factory = sessionmaker(bind=sync_engine)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    # server_default - на уровне БД
    # default - на уровне Python-приложения
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=datetime.datetime.now
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__[:-3].lower()