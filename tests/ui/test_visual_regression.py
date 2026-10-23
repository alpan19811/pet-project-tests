import allure
from playwright.sync_api import expect
from pages.todo_page import TodoPage


@allure.feature("Визуальное регрессионное тестирование")
@allure.story("Проверка скриншотов главной страницы")
def test_homepage_visual_regression(page):
    """Проверяем, что главная страница выглядит как ожидается."""
    todo_page = TodoPage(page)

    with allure.step("Открыть главную страницу"):
        todo_page.open_todo_page()

    with allure.step("Сравнить скриншот с эталоном (baseline)"):
        # Playwright сам создаст эталон при первом запуске.
        # При следующих запусках он сравнит пиксели и упадёт, если есть отличия.
        expect(page).to_have_screenshot("homepage.png")


@allure.feature("Визуальное регрессионное тестирование")
@allure.story("Проверка скриншотов после добавления задачи")
def test_add_todo_visual_regression(page):
    """Проверяем визуальное состояние после добавления задачи."""
    todo_page = TodoPage(page)

    with allure.step("Открыть страницу и добавить задачу"):
        todo_page.open_todo_page()
        todo_page.add_todo("Визуальный тест")

    with allure.step("Сравнить скриншот списка задач с эталоном"):
        expect(page).to_have_screenshot("todo_list_with_item.png")