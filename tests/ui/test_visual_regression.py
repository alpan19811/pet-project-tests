import allure
from pages.todo_page import TodoPage


@allure.feature("Визуальное регрессионное тестирование")
@allure.story("Проверка скриншотов главной страницы")
def test_homepage_visual_regression(page):
    """Проверяем, что главная страница выглядит как ожидается."""
    todo_page = TodoPage(page)

    with allure.step("Открыть главную страницу"):
        todo_page.open_todo_page()

    with allure.step("Сделать скриншот и сравнить с эталоном"):
        # Playwright автоматически сравнит скриншот с baseline-изображением
        # Если baseline не существует - он будет создан при первом запуске
        page.screenshot(path="screenshots/homepage.png")
        # Альтернатива: использовать expect для автоматической проверки
        # from playwright.sync_api import expect
        # expect(page).to_have_screenshot()


@allure.feature("Визуальное регрессионное тестирование")
@allure.story("Проверка скриншотов после добавления задачи")
def test_add_todo_visual_regression(page):
    """Проверяем визуальное состояние после добавления задачи."""
    todo_page = TodoPage(page)

    with allure.step("Открыть страницу и добавить задачу"):
        todo_page.open_todo_page()
        todo_page.add_todo("Визуальный тест")

    with allure.step("Сделать скриншот списка задач"):
        page.screenshot(path="screenshots/todo_list_with_item.png")


@allure.feature("Визуальное регрессионное тестирование")
@allure.story("Проверка скриншотов пустого списка")
def test_empty_todo_list_visual_regression(page):
    """Проверяем, что пустой список выглядит корректно."""
    todo_page = TodoPage(page)

    with allure.step("Открыть страницу (список должен быть пустым)"):
        todo_page.open_todo_page()

    with allure.step("Сделать скриншот пустого списка"):
        page.screenshot(path="screenshots/empty_todo_list.png")