"""Нагрузочное тестирование API с помощью Locust.

Запуск с веб-интерфейсом:
    locust -f load_tests/locustfile.py
    затем открыть http://localhost:8089

Запуск без интерфейса (так будет в CI):
    locust -f load_tests/locustfile.py --headless -u 5 -r 1 -t 15s --only-summary
"""

import os
import random

from locust import HttpUser, between, task


class ApiUser(HttpUser):
    """Виртуальный пользователь: ведёт себя как клиент нашего API."""

    # Locust запускается ОТДЕЛЬНЫМ инструментом (не pytest), поэтому
    # не знает про наш conftest/settings — берём адрес из переменной окружения
    host = os.getenv("BASE_API_URL", "https://reqres.in/api")

    wait_time = between(1, 3)   # пауза 1-3 сек между действиями, как живой человек

    @task(5)
    def browse_user_list(self):
        """Самое частое действие: листать список (вес 5)."""
        self.client.get("/users", params={"page": random.randint(1, 3)}, name="GET /users")

    @task(3)
    def open_user_card(self):
        """Реже: открыть карточку (вес 3)."""
        self.client.get(f"/users/{random.randint(1, 10)}", name="GET /users/:id")

    @task(2)
    def create_user(self):
        """Редко: создать сущность (вес 2)."""
        self.client.post("/users", json={"name": "LoadBot", "job": "loadtest"}, name="POST /users")