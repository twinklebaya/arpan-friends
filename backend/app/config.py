from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./crisis.db"
    admin_token: str = "change-me"

    openrouter_api_key: str = ""
    openrouter_model: str = "openrouter/free"

    cors_origins: str = "http://localhost:5173"

    upload_dir: str = "./uploads"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
