from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from utils import Workload


# Декларативный стиль
class WorkersOrm(Base):
    username: Mapped[str]

    # relationships
    resumes: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<WorkersORM> ID: {self.id}, Username: {self.username}"

    def __str__(self):
        return f"<WorkersORM> ID: {self.id}, Username: {self.username}"


class ResumesOrm(Base):
    title: Mapped[str]
    salary: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))

    # relationships
    worker: Mapped["WorkersOrm"] = relationship(back_populates="resumes")

    def __repr__(self):
        return f"<ResumesORM> ID: {self.id}, Title: {self.title}, Salary: {self.salary}, Workload: {self.workload}, Worker ID: {self.worker_id}"

    def __str__(self):
        return f"<ResumesORM> ID: {self.id}, Title: {self.title}, Salary: {self.salary}, Workload: {self.workload}, Worker ID: {self.worker_id}"
