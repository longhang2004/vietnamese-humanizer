from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    REWRITE_ENABLED: bool = False
    CONTRIBUTIONS_ENABLED: bool = False
    ADMIN_API_ENABLED: bool = False
    GEMINI_API_KEY: str | None = None
    ADMIN_API_KEY: str | None = None
    DATABASE_URL: str = "sqlite:///./dev.db"
    TRUSTED_PROXY_HOSTS: str = "127.0.0.1,localhost,::1"
    TRUST_PRIVATE_PROXIES: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
