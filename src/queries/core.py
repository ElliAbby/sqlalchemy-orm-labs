from sqlalchemy import text

from database import sync_engine
from models import metadata_obj

def create_tables():
    metadata_obj.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    metadata_obj.echo = True


def insert_data():
    with sync_engine.connect() as conn:
        stmt = "INSERT INTO workers (username) VALUES ('John Doe'), ('Ivan Ivanov');"
        conn.execute(text(stmt))
        conn.commit()


def select_data():
    with sync_engine.connect() as conn:
        stmt = "SELECT * FROM workers;"
        result = conn.execute(text(stmt))
        for row in result:
            print(row)
