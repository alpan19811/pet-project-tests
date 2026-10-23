import allure


@allure.feature("Список задач")
@allure.story("Добавление и выполнение задачи")
def test_add_and_complete_todo(todo_page):
    with allure.step("Открыть страницу задач"):
        todo_page.open_todo_page()

    with allure.step("Добавить задачу 'Купить хлеб'"):
        todo_page.add_todo("Купить хлеб")

    with allure.step("Проверить, что задача появилась в списке"):
        todo_page.assert_todo_in_list("Купить хлеб")

    with allure.step("Отметить задачу выполненной"):
        todo_page.complete_todo("Купить хлеб")

    with allure.step("Открыть фильтр 'Active'"):
        todo_page.filter_active()

    with allure.step("Проверить, что выполненная задача скрыта из активных"):
        todo_page.assert_todo_not_in_list("Купить хлеб")