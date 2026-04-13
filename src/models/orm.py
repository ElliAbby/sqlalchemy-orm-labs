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

    def __repr__(self):
        return f"ID: {self.id}, Title: {self.title}, Salary: {self.salary}, Workload: {self.workload}, Worker ID: {self.worker_id}"

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Salary: {self.salary}, Workload: {self.workload}, Worker ID: {self.worker_id}"
