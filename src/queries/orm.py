from sqlalchemy import select

from database import Base, session_factory, sync_engine
from models.orm import WorkersOrm


def create_tables():
    # sync_engine.echo = False
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    # sync_engine.echo = True


def insert_data():
    with session_factory() as session:
        try:
            worker1 = WorkersOrm(username="John Doe")
            worker2 = WorkersOrm(username="Ivan Ivanov")
            session.add_all([worker1, worker2])
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при вставке: {e}")


def select_data():
    with session_factory() as session:
        stmt = select(WorkersOrm)
        workers = session.scalars(stmt).all()
        for worker in workers:
            print(f"ID: {worker.id}, Name: {worker.username}")
