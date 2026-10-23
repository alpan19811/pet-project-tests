from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Все настройки проекта в одном месте."""

    # --- UI (Playwright) ---
    base_ui_url: str = "https://demo.playwright.dev/todomvc/"

    # --- API (requests) ---
    base_api_url: str = "https://reqres.in/api"
    api_timeout: int = 10

    # --- Поведение браузера ---
    headless: bool = True

    @field_validator("base_ui_url", "base_api_url")
    @classmethod
    def check_absolute_url(cls, value: str) -> str:
        """URL без схемы http(s):// — почти всегда опечатка. Падаем сразу."""
        if not value.startswith(("http://", "https://")):
            raise ValueError(
                f"URL должен начинаться с http:// или https://, получено: '{value}'. Проверь .env"
            )
        return value

    model_config = SettingsConfigDict(
        env_file=".env",           # откуда читать переменные
        env_file_encoding="utf-8",
        extra="ignore",            # не падать, если в .env есть лишние переменные
    )


# Единственный экземпляр настроек на весь проект
settings = Settings()