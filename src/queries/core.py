from sqlalchemy import delete, insert, select, text, update

from database import sync_engine
from models import metadata_obj, workers_table


class SyncCore:
    @staticmethod
    def create_tables():
        # sync_engine.echo = False
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        # sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with sync_engine.connect() as conn:
            # stmt = "INSERT INTO workers (username) VALUES ('John Doe'), ('Ivan Ivanov');"
            stmt = insert(workers_table).values(
                [
                    {"username": "John Doe"},
                    {"username": "Ivan Ivanov"},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            # stmt = "SELECT * FROM workers;"
            stmt = select(workers_table)
            result = conn.execute(stmt)
            for row in result:
                print(row)

    @staticmethod
    def update_worker(worker_id: int, new_username: str):
        with sync_engine.connect() as conn:
            # stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            # stmt = stmt.bindparams(username=new_username, id=worker_id)
            stmt = (
                update(workers_table)
                .values(username=new_username)
                .filter_by(id=worker_id)
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def delete_worker(worker_id: int):
        with sync_engine.connect() as conn:
            # stmt = text("DELETE FROM workers WHERE id=:id")
            # stmt = stmt.bindparams(id=worker_id)
            stmt = delete(workers_table).filter_by(id=worker_id)
            conn.execute(stmt)
            conn.commit()
