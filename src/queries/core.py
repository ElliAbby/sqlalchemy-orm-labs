from sqlalchemy import text, insert, select

from database import sync_engine
from models import metadata_obj, workers_table


def create_tables():
    # sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    # sync_engine.echo = True


def insert_data():
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


def select_data():
    with sync_engine.connect() as conn:
        # stmt = "SELECT * FROM workers;"
        stmt = select(workers_table)
        result = conn.execute(stmt)
        for row in result:
            print(row)
