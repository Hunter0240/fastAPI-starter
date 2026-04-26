from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/app"
    secret_key: str = "change-me-in-production"
    access_token_expire: int = 30
    refresh_token_expire: int = 7
    cors_origins: str = "http://localhost:5173"
    rate_limit_max: int = 100
    rate_limit_window: int = 60
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "extra": "ignore"}

    @model_validator(mode="after")
    def _check_secret_key(self):
        if self.secret_key == "change-me-in-production" or len(self.secret_key) < 32:
            raise ValueError(
                "SECRET_KEY must be set to a strong value (at least 32 characters). "
                "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(48))\""
            )
        return self


settings = Settings()
