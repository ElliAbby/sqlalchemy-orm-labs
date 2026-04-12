from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from utils import Workload


# Декларативный стиль
class WorkersOrm(Base):
    username: Mapped[str]


class ResumesOrm(Base):
    title: Mapped[str]
    salary: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
