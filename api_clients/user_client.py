import allure

from core.base_api import BaseAPIClient


class UserClient(BaseAPIClient):
    """Клиент ресурса /users: бизнес-методы поверх базового HTTP-клиента.

    Аналог Page Object, но для API: тесты не знают ни эндпоинтов,
    ни структуры тел запросов — они вызывают методы этого класса.
    """

    ENDPOINT = "/users"

    # ---------- ЧТЕНИЕ (GET) ----------

    @allure.step("Получить список пользователей (страница {page})")
    def get_users(self, page: int = 1):
        return self.get(self.ENDPOINT, params={"page": page})

    @allure.step("Получить пользователя с id={user_id}")
    def get_user(self, user_id: int):
        return self.get(f"{self.ENDPOINT}/{user_id}")

    # ---------- СОЗДАНИЕ (POST) ----------

    @allure.step("Создать пользователя: name={name}, job={job}")
    def create_user(self, name: str, job: str):
        return self.post(self.ENDPOINT, json={"name": name, "job": job})

    # ---------- ОБНОВЛЕНИЕ (PUT / PATCH) ----------

    @allure.step("Полностью обновить пользователя id={user_id} (PUT)")
    def update_user(self, user_id: int, name: str, job: str):
        return self.put(f"{self.ENDPOINT}/{user_id}", json={"name": name, "job": job})

    @allure.step("Частично обновить пользователя id={user_id} (PATCH): job={job}")
    def patch_user(self, user_id: int, job: str):
        return self.patch(f"{self.ENDPOINT}/{user_id}", json={"job": job})

    # ---------- УДАЛЕНИЕ (DELETE) ----------

    @allure.step("Удалить пользователя id={user_id}")
    def delete_user(self, user_id: int):
        return self.delete(f"{self.ENDPOINT}/{user_id}")