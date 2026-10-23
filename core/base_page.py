from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Базовая страница: общий технический слой для всех Page Object'ов.

    Здесь лежат универсальные действия с браузером и элементами:
    открыть, кликнуть, ввести, проверить. Наследники (конкретные страницы)
    добавляют только свои локаторы и бизнес-сценарии.
    """

    def __init__(self, page: Page):
        self.page = page

    # ---------- Навигация ----------

    def open(self, url: str) -> None:
        """Открыть страницу по URL."""
        self.page.goto(url)

    # ---------- Действия с элементами ----------

    def click(self, locator: Locator) -> None:
        """Клик по элементу."""
        locator.click()

    def fill(self, locator: Locator, text: str) -> None:
        """Ввести текст в поле. ВАЖНО: fill сам сначала очищает поле."""
        locator.fill(text)

    def clear(self, locator: Locator) -> None:
        """Очистить поле."""
        locator.clear()

    def type_text(self, locator: Locator, text: str, delay: int = 50) -> None:
        """Печатать посимвольно, как человек (для автокомплита, масок)."""
        locator.press_sequentially(text, delay=delay)

    def press_key(self, locator: Locator, key: str) -> None:
        """Нажать клавишу: 'Enter', 'Tab', 'Escape' и т.п."""
        locator.press(key)

    def hover(self, locator: Locator) -> None:
        """Навести курсор (для всплывающих меню и подсказок)."""
        locator.hover()

    def select_option(self, locator: Locator, value: str) -> None:
        """Выбрать значение в выпадающем списке <select>."""
        locator.select_option(value=value)

    def check(self, locator: Locator) -> None:
        """Гарантированно включить чекбокс."""
        locator.check()

    def uncheck(self, locator: Locator) -> None:
        """Гарантированно выключить чекбокс."""
        locator.uncheck()

    # ---------- Чтение данных со страницы ----------

    def get_text(self, locator: Locator) -> str:
        """Видимый текст элемента."""
        return locator.inner_text()

    def get_value(self, locator: Locator) -> str:
        """Текущее значение поля ввода."""
        return locator.input_value()

    def is_visible(self, locator: Locator) -> bool:
        """Мгновенный снимок: виден ли элемент СЕЙЧАС (без ожидания!)."""
        return locator.is_visible()

    # ---------- Проверки (assertions) ----------

    def assert_visible(self, locator: Locator, timeout: int = 5000) -> None:
        expect(locator).to_be_visible(timeout=timeout)

    def assert_hidden(self, locator: Locator, timeout: int = 5000) -> None:
        expect(locator).to_be_hidden(timeout=timeout)

    def assert_text(self, locator: Locator, expected: str, timeout: int = 5000) -> None:
        expect(locator).to_contain_text(expected, timeout=timeout)

    def assert_checked(self, locator: Locator, timeout: int = 5000) -> None:
        expect(locator).to_be_checked(timeout=timeout)


