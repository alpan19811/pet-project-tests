import pytest

from config.settings import settings
from pages.todo_page import TodoPage


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """Переопределяем параметры ЗАПУСКА БРАУЗЕРА из pytest-playwright.

    Берём дефолтные аргументы плагина и подмешиваем наш headless из .env.
    """
    return {**browser_type_launch_args, "headless": settings.headless}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Настройки 'профиля': фиксированный размер окна для стабильности тестов."""
    return {**browser_context_args, "viewport": {"width": 1280, "height": 720}}


@pytest.fixture
def todo_page(page) -> TodoPage:
    """Готовый Page Object для тестов: тест не создаёт его сам."""
    return TodoPage(page)