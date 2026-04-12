from pathlib import Path

# from pydantic_core.core_schema import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DB_NAME: str = "database"
    DB_ECHO: bool = False

    @property
    def db_url(self):
        return f"sqlite:///{BASE_DIR}/{self.DB_NAME}.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
