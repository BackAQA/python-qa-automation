
import os
from dataclasses import dataclass

from dotenv import load_dotenv


# Загружаем настройки из файла .env
load_dotenv()


def _get_base_url() -> str:
    """Получает и проверяет базовый адрес API."""

    base_url = os.getenv(
        "API_BASE_URL",
        "https://automationexercise.com"
    ).strip().rstrip("/")

    if not base_url:
        raise ValueError(
            "Настройка API_BASE_URL не может быть пустой."
        )

    if not base_url.startswith(("http://", "https://")):
        raise ValueError(
            "Настройка API_BASE_URL должна начинаться с http:// или https://."
        )

    return base_url


def _get_timeout() -> float:
    """Получает и проверяет время ожидания ответа от сервера."""

    timeout_value = os.getenv("API_TIMEOUT", "10")

    try:
        timeout = float(timeout_value)
    except ValueError as error:
        raise ValueError(
            "Настройка API_TIMEOUT должна содержать число."
        ) from error

    if timeout <= 0:
        raise ValueError(
            "Настройка API_TIMEOUT должна быть больше нуля."
        )

    return timeout


@dataclass(frozen=True)
class Settings:
    """Хранит настройки автоматизированного тестирования."""

    api_base_url: str
    api_timeout: float


def load_settings() -> Settings:
    """Создаёт объект с настройками проекта."""

    return Settings(
        api_base_url=_get_base_url(),
        api_timeout=_get_timeout()
    )


# Общие настройки проекта
settings = load_settings()
