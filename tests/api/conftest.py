import pytest

from api_clients.user_client import UserClient


@pytest.fixture(scope="session")
def user_client() -> UserClient:
    """Готовый клиент /users, один на весь прогон.

    scope='session' означает:
    - до yield: создали клиента один раз при первом запросе теста;
    - после yield: закрыли TCP-соединения после окончания ВСЕХ тестов.

    Почему session, а не function?
    - Сессия requests переиспользует TCP-соединения с сервером → быстрее.
    - У reqres нет кукисов/сессий, перетекающих между тестами,
      поэтому изоляция тестов НЕ нарушается.
    """
    client = UserClient()
    yield client            # ← вот здесь "держи, тест, клиента"
    client.close()          # ← teardown: закрыли сессию после всего прогона