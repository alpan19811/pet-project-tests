import allure
from playwright.sync_api import Locator

from config.settings import settings
from core.base_page import BasePage


class TodoPage(BasePage):
    """Page Object страницы списка задач (todomvc).

    Хранит локаторы страницы и бизнес-действия над ними.
    Тесты будут общаться ТОЛЬКО с этим классом и ничего
    не знать про Playwright и локаторы.
    """

    # ================= ЛОКАТОРЫ =================

    @property
    def new_todo_input(self) -> Locator:
        """Поле ввода задачи: поиск по тексту-плейсхолдеру."""
        return self.page.get_by_placeholder("What needs to be done?")

    @property
    def todo_items(self) -> Locator:
        """Все задачи в списке: поиск по CSS-селектору."""
        return self.page.locator(".todo-list li")

    @property
    def toggle_all_checkbox(self) -> Locator:
        """Чекбокс 'отметить всё': поиск по тексту label."""
        return self.page.get_by_label("Mark all as complete")

    @property
    def clear_completed_button(self) -> Locator:
        """Кнопка 'Clear completed': поиск по роли и имени."""
        return self.page.get_by_role("button", name="Clear completed")

    @property
    def items_left_counter(self) -> Locator:
        """Счётчик оставшихся задач."""
        return self.page.locator(".todo-count")

    @property
    def filter_active_link(self) -> Locator:
        """Ссылка-фильтр 'Active'."""
        return self.page.get_by_role("link", name="Active")

    def todo_item(self, title: str) -> Locator:
        """Конкретная задача: фильтруем все задачи по тексту."""
        return self.todo_items.filter(has_text=title)

    def todo_checkbox(self, title: str) -> Locator:
        """Чекбокс конкретной задачи."""
        return self.todo_item(title).get_by_role("checkbox")

    def todo_delete_button(self, title: str) -> Locator:
        """Кнопка удаления конкретной задачи (появляется при наведении)."""
        return self.todo_item(title).locator(".destroy")

    # ================= БИЗНЕС-ДЕЙСТВИЯ =================

    @allure.step("Открыть страницу задач")
    def open_todo_page(self) -> None:
        self.open(settings.base_ui_url)

    @allure.step("Добавить задачу: {title}")
    def add_todo(self, title: str) -> None:
        self.fill(self.new_todo_input, title)
        self.press_key(self.new_todo_input, "Enter")

    @allure.step("Отметить задачу выполненной: {title}")
    def complete_todo(self, title: str) -> None:
        self.check(self.todo_checkbox(title))

    @allure.step("Удалить задачу: {title}")
    def delete_todo(self, title: str) -> None:
        self.hover(self.todo_item(title))          # кнопка удаления скрыта до наведения
        self.click(self.todo_delete_button(title))

    @allure.step("Удалить все выполненные задачи")
    def clear_completed(self) -> None:
        self.click(self.clear_completed_button)

    @allure.step("Показать только активные задачи")
    def filter_active(self) -> None:
        self.click(self.filter_active_link)

    # ================= ЧТЕНИЕ ДАННЫХ =================

    @allure.step("Получить список всех задач")
    def get_todo_titles(self) -> list[str]:
        return self.todo_items.all_inner_texts()

    @allure.step("Получить текст счётчика оставшихся задач")
    def get_items_left(self) -> str:
        return self.get_text(self.items_left_counter)

    # ================= ПРОВЕРКИ =================

    @allure.step("Проверить, что задача есть в списке: {title}")
    def assert_todo_in_list(self, title: str) -> None:
        self.assert_visible(self.todo_item(title))

    @allure.step("Проверить, что задачи нет в списке: {title}")
    def assert_todo_not_in_list(self, title: str) -> None:
        self.assert_hidden(self.todo_item(title))