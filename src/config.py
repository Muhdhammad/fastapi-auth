from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./user.db"

    JWT_SECRET_KEY: str
    JWT_ALGO: str

    TOKEN_SECRET_KEY: str

    FRONTEND_URL: str

    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int

    model_config = SettingsConfigDict(env_file=str(SRC_DIR / ".env"), extra="ignore")

Config = Settings()