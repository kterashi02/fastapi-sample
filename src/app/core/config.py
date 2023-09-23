from pydantic_settings import BaseSettings
import os
import secrets


class Settings(BaseSettings):
    MYSQL_USER: str = os.environ["MYSQL_USER"]
    MYSQL_PASSWORD: str = os.environ["MYSQL_PASSWORD"]
    MYSQL_HOST: str = os.environ["MYSQL_HOST"]
    MYSQL_DB: str = os.environ["MYSQL_DATABASE"]
    SECRET_KEY: str = secrets.token_urlsafe(32)

    SQLALCHEMY_DATABASE_URI: str = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    )

    class Config:
        case_sensitive = True


settings = Settings()
