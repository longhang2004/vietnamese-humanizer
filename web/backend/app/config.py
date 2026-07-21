from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    GEMINI_API_KEY: str | None = None
    ADMIN_API_KEY: str = "change_this_secret_admin_key"
    DATABASE_URL: str = "sqlite:///./dev.db"
    LINT_MAX_CHARS: int = 20000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
