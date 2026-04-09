from sqlalchemy import create_engine, text

DB_URL = "sqlite:///./database.db"

engine = create_engine(DB_URL, echo=True)

# в конце ROLLBACK
with engine.connect() as conn:
    result = conn.execute(text("SELECT 'Hello World'"))
    print(f"Result: {result.scalar()}")

# в конце COMMIT
with engine.begin() as conn:
    result = conn.execute(text("SELECT 'Hello World'"))
    print(f"Result: {result.scalar()}")