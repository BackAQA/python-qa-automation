
import re

import allure
import pytest

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


@allure.epic("Python QA Automation Framework")
@allure.feature("API + UI Integration")
@allure.story("Позитивная авторизация")
@allure.title(
    "Пользователь, созданный через API, может войти через UI"
)
@pytest.mark.integration
def test_user_created_via_api_can_login_via_ui(
    api_registered_user: dict[str, str],
    page: Page
) -> None:

    # Создаём Page Object страницы авторизации
    login_page = LoginPage(page)

    # Шаг 1. Открываем страницу авторизации
    with allure.step("Открываем страницу авторизации"):
        login_page.open()

    # Шаг 2. Выполняем вход с данными API-пользователя
    with allure.step("Выполняем вход с данными API-пользователя"):
        login_page.login(
            email=api_registered_user["email"],
            password=api_registered_user["password"]
        )

    # Шаг 3. Проверяем успешную авторизацию
    with allure.step("Проверяем успешную авторизацию пользователя"):

        login_page.should_be_logged_in_as(
            api_registered_user["name"]
        )

        # Проверяем наличие кнопки выхода
        expect(login_page.logout_link).to_be_visible()

        # Проверяем наличие ссылки удаления аккаунта
        expect(login_page.delete_account_link).to_be_visible()


@allure.epic("Python QA Automation Framework")
@allure.feature("API + UI Integration")
@allure.story("Негативная авторизация")
@allure.title(
    "Пользователь, созданный через API, не может войти с неправильным паролем"
)
@pytest.mark.integration
def test_user_created_via_api_cannot_login_with_invalid_password(
    api_registered_user: dict[str, str],
    page: Page
) -> None:

    # Создаём Page Object страницы авторизации
    login_page = LoginPage(page)

    # Подготавливаем неправильный пароль
    wrong_password = f"{api_registered_user['password']}_wrong"

    # Шаг 1. Открываем страницу авторизации
    with allure.step("Открываем страницу авторизации"):
        login_page.open()

    # Шаг 2. Выполняем вход с неправильным паролем
    with allure.step("Пытаемся войти с неправильным паролем"):
        login_page.login(
            email=api_registered_user["email"],
            password=wrong_password
        )

    # Шаг 3. Проверяем сообщение об ошибке
    with allure.step("Проверяем сообщение об ошибке авторизации"):
        login_page.should_show_login_error()

    # Шаг 4. Проверяем, что пользователь не авторизован
    with allure.step("Проверяем отсутствие авторизованного состояния"):

        # Пользователь должен остаться на странице авторизации
        expect(page).to_have_url(
            re.compile(r"/login/?$")
        )

        # Ссылка выхода не должна отображаться
        expect(login_page.logout_link).to_have_count(0)

        # Сообщение об авторизованном пользователе отсутствует
        expect(login_page.logged_in_message).to_have_count(0)
