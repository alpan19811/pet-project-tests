import allure
import requests
from requests import Response

from config.settings import settings


class BaseAPIClient:
    """Базовый HTTP-клиент: общая логика для всех API-клиентов проекта.

    Отвечает за: склейку URL, переиспользование соединений (Session),
    единый таймаут, логирование запросов и ответов в Allure.
    НЕ отвечает за проверки (assert) — их пишут тесты.
    """

    def __init__(self, base_url: str | None = None, timeout: int | None = None):
        self.base_url = (base_url or settings.base_api_url).rstrip("/")
        self.timeout = timeout or settings.api_timeout
        self.session = requests.Session()

    # ---------- СЛУЖЕБНЫЕ МЕТОДЫ ----------

    def _build_url(self, endpoint: str) -> str:
        """Склеить base_url и endpoint без двойных слэшей."""
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _log_to_allure(self, response: Response) -> None:
        """Приложить запрос и ответ к отчёту: дебаг в CI без воспроизведения локально."""
        allure.attach(
            f"{response.request.method} {response.url}\n"
            f"--- request body: {response.request.body}\n"
            f"--- status: {response.status_code}\n"
            f"--- response body: {response.text}",
            name=f"{response.request.method} {response.url}",
            attachment_type=allure.attachment_type.TEXT,
        )

    # ---------- HTTP-МЕТОДЫ ----------

    @allure.step("GET {endpoint}")
    def get(self, endpoint: str, params: dict | None = None, **kwargs) -> Response:
        response = self.session.get(
            self._build_url(endpoint), params=params, timeout=self.timeout, **kwargs
        )
        self._log_to_allure(response)
        return response

    @allure.step("POST {endpoint}")
    def post(self, endpoint: str, json: dict | None = None, **kwargs) -> Response:
        response = self.session.post(
            self._build_url(endpoint), json=json, timeout=self.timeout, **kwargs
        )
        self._log_to_allure(response)
        return response

    @allure.step("PUT {endpoint}")
    def put(self, endpoint: str, json: dict | None = None, **kwargs) -> Response:
        response = self.session.put(
            self._build_url(endpoint), json=json, timeout=self.timeout, **kwargs
        )
        self._log_to_allure(response)
        return response

    @allure.step("PATCH {endpoint}")
    def patch(self, endpoint: str, json: dict | None = None, **kwargs) -> Response:
        response = self.session.patch(
            self._build_url(endpoint), json=json, timeout=self.timeout, **kwargs
        )
        self._log_to_allure(response)
        return response

    @allure.step("DELETE {endpoint}")
    def delete(self, endpoint: str, **kwargs) -> Response:
        response = self.session.delete(self._build_url(endpoint), timeout=self.timeout, **kwargs)
        self._log_to_allure(response)
        return response

    # ---------- ЗАГОЛОВКИ И АВТОРИЗАЦИЯ ----------

    def set_headers(self, headers: dict) -> None:
        """Добавить заголовки сразу ко всем будущим запросам сессии."""
        self.session.headers.update(headers)

    def set_bearer_token(self, token: str) -> None:
        """Типовой способ авторизации: токен одним заголовком на всю сессию."""
        self.session.headers["Authorization"] = f"Bearer {token}"

    def close(self) -> None:
        self.session.close()