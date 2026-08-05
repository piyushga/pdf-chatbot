from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    frontend_origin: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
