import json

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_access_key: str = Field("", validation_alias="API_ACCESS_KEY")

    cors_origins_raw: str = Field("*", validation_alias="CORS_ORIGINS")

    @property
    def cors_origins(self) -> list[str]:
        text = self.cors_origins_raw.strip()
        if text.startswith("["):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
        return [origin.strip() for origin in text.split(",") if origin.strip()]


settings = Settings()
