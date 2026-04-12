from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from utils import Workload


# Императивный стиль
metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)


# Декларативный стиль
class WorkersOrm(Base):
    username: Mapped[str]


class ResumesOrm(Base):
    title: Mapped[str]
    salary: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))