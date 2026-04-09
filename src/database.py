from sqlalchemy import create_engine, text

from config import settings

sync_engine = create_engine(settings.DB_URL, echo=True)
