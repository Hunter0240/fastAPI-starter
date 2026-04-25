from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./app.db"
    secret_key: str = "change-me-in-production"
    access_token_expire: int = 30
    refresh_token_expire: int = 7
    cors_origins: str = "*"
    rate_limit_max: int = 100
    rate_limit_window: int = 60
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
