import allure
from faker import Faker

fake = Faker()


@allure.feature("API: Пользователи")
@allure.story("Чтение (GET)")
def test_get_users_list_with_pagination(user_client):
    with allure.step("Запросить страницу 2 списка пользователей"):
        response = user_client.get_users(page=2)

    with allure.step("Проверить статус и пагинацию"):
        assert response.status_code == 200
        body = response.json()
        assert body["page"] == 2
        assert len(body["data"]) > 0


@allure.feature("API: Пользователи")
@allure.story("Чтение (GET)")
def test_get_single_user(user_client):
    with allure.step("Запросить пользователя с id=2"):
        response = user_client.get_user(user_id=2)

    with allure.step("Проверить статус и поля карточки"):
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["id"] == 2
        assert "email" in data


@allure.feature("API: Пользователи")
@allure.story("Создание (POST)")
def test_create_user(user_client):
    name, job = fake.name(), fake.job()

    with allure.step(f"Создать пользователя: {name} / {job}"):
        response = user_client.create_user(name=name, job=job)

    with allure.step("Проверить 201 и эхо полезной нагрузки"):
        assert response.status_code == 201
        body = response.json()
        assert body["name"] == name          # сервер вернул то, что отправили
        assert body["job"] == job
        assert body["id"]                    # сервер выдал id
        assert body["createdAt"]             # и метку времени


@allure.feature("API: Пользователи")
@allure.story("Обновление (PUT)")
def test_update_user_full(user_client):
    with allure.step("Подготовить данные: создать пользователя"):
        user_id = user_client.create_user(name="Before", job="qa").json()["id"]

    with allure.step("Полностью обновить через PUT"):
        response = user_client.update_user(user_id=user_id, name="After", job="manager")

    with allure.step("Проверить 200 и updatedAt"):
        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "After"
        assert body["updatedAt"]


@allure.feature("API: Пользователи")
@allure.story("Обновление (PATCH)")
def test_update_user_partial(user_client):
    with allure.step("Подготовить данные: создать пользователя"):
        user_id = user_client.create_user(name="Patch Me", job="qa").json()["id"]

    with allure.step("Частично обновить через PATCH (только job)"):
        response = user_client.patch_user(user_id=user_id, job="director")

    with allure.step("Проверить 200 и updatedAt"):
        assert response.status_code == 200
        assert response.json()["updatedAt"]


@allure.feature("API: Пользователи")
@allure.story("Удаление (DELETE)")
def test_delete_user(user_client):
    with allure.step("Подготовить данные: создать пользователя"):
        user_id = user_client.create_user(name="Doomed", job="qa").json()["id"]

    with allure.step("Удалить пользователя"):
        response = user_client.delete_user(user_id=user_id)

    with allure.step("Проверить 204 и ПУСТОЕ тело"):
        assert response.status_code == 204
        assert response.text == ""


@allure.feature("API: Пользователи")
@allure.story("Негативный сценарий")
def test_get_non_existent_user_returns_404(user_client):
    with allure.step("Запросить заведомо несуществующего пользователя"):
        response = user_client.get_user(user_id=999999)

    with allure.step("Проверить 404"):
        assert response.status_code == 404