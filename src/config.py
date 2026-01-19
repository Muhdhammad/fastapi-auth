from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./user.db"

    JWT_SECRET_KEY: str
    JWT_ALGO: str

    TOKEN_SECRET_KEY: str

    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

Config = Settings()