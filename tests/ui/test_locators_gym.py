"""Тренажёр локаторов и действий.

Страница собирается из ЛОКАЛЬНОЙ HTML-строки через page.set_content:
без интернета, без сервера, со 100% предсказуемым DOM.
ВАЖНО: локаторы прямо в тесте допустимы ТОЛЬКО здесь, как учебное упражнение.
В боевых тестах они живут в Page Object'ах.
"""

import allure
import pytest

from core.base_page import BasePage

GYM_HTML = """
<h1>Тренажёр локаторов</h1>

<input placeholder="Введите имя пользователя">

<button data-testid="submit-btn">Отправить</button>
<button aria-label="Закрыть окно">X</button>

<p>Секретное сообщение</p>

<input type="checkbox" id="agree">
<label for="agree">Согласен с правилами</label>

<select data-testid="city-select">
    <option value="">-- Выберите город --</option>
    <option value="msk">Москва</option>
    <option value="spb">Санкт-Петербург</option>
</select>

<input id="search" placeholder="Поиск...">
<p id="search-result"></p>

<div data-testid="hover-zone" style="width:120px;height:40px;border:1px solid black">
    Наведи курсор
</div>
<p id="tooltip" style="display:none">Тултип появился!</p>

<script>
    const search = document.getElementById('search');
    const result = document.getElementById('search-result');
    search.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') result.textContent = 'Найдено: ' + search.value;
        if (e.key === 'Escape') search.value = '';
    });
    const zone = document.querySelector('[data-testid="hover-zone"]');
    const tooltip = document.getElementById('tooltip');
    zone.addEventListener('mouseenter', () => tooltip.style.display = 'block');
    zone.addEventListener('mouseleave', () => tooltip.style.display = 'none');
</script>
"""


@pytest.fixture
def gym_page(page) -> BasePage:
    """Страница с загруженным HTML тренажёра (сеть не нужна)."""
    page.set_content(GYM_HTML)
    return BasePage(page)


@allure.feature("Тренажёр")
@allure.story("Виды локаторов")
def test_locators_placeholder_testid_role_text_label(gym_page):
    with allure.step("Локатор по плейсхолдеру: ввести имя"):
        gym_page.fill(gym_page.page.get_by_placeholder("Введите имя пользователя"), "john.doe")

    with allure.step("Локатор по test-id: кликнуть кнопку"):
        gym_page.click(gym_page.page.get_by_test_id("submit-btn"))

    with allure.step("Локатор по роли и имени (aria-label): кнопка на месте"):
        gym_page.assert_visible(gym_page.page.get_by_role("button", name="Закрыть окно"))

    with allure.step("Локатор по тексту: сообщение видно"):
        gym_page.assert_visible(gym_page.page.get_by_text("Секретное сообщение"))

    with allure.step("Локатор по label: отметить чекбокс"):
        agree = gym_page.page.get_by_label("Согласен с правилами")
        gym_page.check(agree)
        gym_page.assert_checked(agree)


@allure.feature("Тренажёр")
@allure.story("Выпадающий список и поле ввода")
def test_select_and_input_actions(gym_page):
    city_select = gym_page.page.get_by_test_id("city-select")
    search_field = gym_page.page.locator("#search")

    with allure.step("Выпадающий список: выбрать город по value"):
        gym_page.select_option(city_select, "spb")
        assert gym_page.get_value(city_select) == "spb"

    with allure.step("Посимвольный ввод, как человек"):
        gym_page.type_text(search_field, "playwright", delay=30)
        assert gym_page.get_value(search_field) == "playwright"

    with allure.step("Клавиша Enter: поиск 'сработал'"):
        gym_page.press_key(search_field, "Enter")
        gym_page.assert_text(gym_page.page.locator("#search-result"), "Найдено: playwright")

    with allure.step("Клавиша Escape: поле очистилось (JS страницы)"):
        gym_page.press_key(search_field, "Escape")
        assert gym_page.get_value(search_field) == ""

    with allure.step("clear(): поле пустое"):
        gym_page.type_text(search_field, "временный текст")
        gym_page.clear(search_field)
        assert gym_page.get_value(search_field) == ""


@allure.feature("Тренажёр")
@allure.story("Наведение мыши")
def test_hover_shows_tooltip(gym_page):
    with allure.step("Навести курсор на зону"):
        gym_page.hover(gym_page.page.get_by_test_id("hover-zone"))

    with allure.step("Тултип стал видимым"):
        gym_page.assert_visible(gym_page.page.locator("#tooltip"))