import json
import re

from pathlib import Path
from typing import Iterator
from uuid import uuid4

import allure
import pytest
from playwright.sync_api import Page, expect

from api.clients.api_client import ApiClient
from api.endpoints.users import (
    CREATE_ACCOUNT,
    DELETE_ACCOUNT,
    USER_DETAILS
)
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from utils.config import settings

@pytest.fixture
def registered_user(page: Page) -> Iterator[dict[str, str]]:
    """
    Creates a new test user, authenticates it
    and deletes the account after the test.
    """

    login_page = LoginPage(page)
    signup_page = SignupPage(page)

    # Test user data
    user = {
        "name": "QA Automation Fixture",
        "email": f"qa.fixture.{uuid4().hex}@example.invalid",
        "password": "TestPassword123!"
    }

    account_created = False

    try:
        # SETUP: open signup page
        login_page.open()

        # Start registration
        login_page.signup(
            name=user["name"],
            email=user["email"]
        )

        # Fill account information
        signup_page.fill_account_information(
            password=user["password"],
            day="10",
            month="May",
            year="1995",
            title="Mr"
        )

        # Set preferences
        signup_page.set_preferences(
            newsletter=False,
            special_offers=False
        )

        # Fill address information
        signup_page.fill_address_information(
            first_name="QA",
            last_name="Automation",
            address1="123 Test Street",
            country="United States",
            state="California",
            city="San Francisco",
            zipcode="94103",
            mobile_number="4155550100"
        )

        # Create account
        signup_page.create_account()

        account_created_message = page.locator('[data-qa="account-created"]')

        expect(account_created_message).to_be_visible()
        expect(account_created_message).to_contain_text("Account Created!")

        account_created = True

        # Continue to homepage
        page.get_by_role(
            "link",
            name="Continue",
            exact=True
        ).click()

        # Verify authentication
        login_page.should_be_logged_in_as(user["name"])

        # Pass user data to the test
        yield user

    finally:
        # TEARDOWN: clean up the created account
        if account_created:

            # If the test logged out, authenticate again
            # before deleting the account.
            if not login_page.logout_link.is_visible():

                login_page.open()

                login_page.login(
                    email=user["email"],
                    password=user["password"]
                )

                login_page.should_be_logged_in_as(user["name"])

            # Delete the test account
            login_page.delete_account()

            account_deleted_message = page.locator('[data-qa="account-deleted"]')

            expect(account_deleted_message).to_be_visible()
            expect(account_deleted_message).to_contain_text("Account Deleted!")

@pytest.fixture
def api_client() -> Iterator[ApiClient]:
    """
    Создаёт общий API-клиент.
    После завершения теста сохраняет историю запросов в Allure
    и закрывает HTTP-сессию.
    """

    client = ApiClient(
        base_url=settings.api_base_url,
        timeout=settings.api_timeout
    )

    try:
        yield client

    finally:
        try:
            # Прикладываем историю API-запросов к отчёту Allure
            if client.request_history:

                allure.attach(
                    json.dumps(
                        client.request_history,
                        ensure_ascii=False,
                        indent=4
                    ),
                    name="История API-запросов",
                    attachment_type=allure.attachment_type.JSON
                )

        finally:
            # Закрываем HTTP-сессию
            client.close()

@pytest.fixture
def api_registered_user(
    api_client: ApiClient
) -> Iterator[dict[str, str]]:
    """
    Создаёт тестового пользователя через API
    и удаляет его после завершения теста.
    """

    # Генерируем уникальный email
    email = f"qa.automation.{uuid4().hex}@example.com"

    # Подготавливаем данные тестового пользователя
    user_data = {
        "name": "QA Automation Tester",
        "email": email,
        "password": "TestPassword123!",
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "5",
        "birth_year": "1995",
        "firstname": "QA",
        "lastname": "Tester",
        "company": "QA Automation",
        "address1": "Test Street 10",
        "address2": "Office 1",
        "country": "United States",
        "zipcode": "10001",
        "state": "New York",
        "city": "New York",
        "mobile_number": "1234567890"
    }

    # Отмечаем, был ли пользователь создан
    account_created = False

    try:
        # SETUP: создаём пользователя через API
        create_response = api_client.post(
            CREATE_ACCOUNT,
            data=user_data
        )

        create_data = create_response.json()

        account_created = create_data.get("responseCode") == 201

        # Проверяем HTTP-статус
        assert create_response.status_code == 200, (
            f"Ожидался HTTP-статус 200 при создании пользователя, "
            f"получен {create_response.status_code}. "
            f"Ответ: {create_response.text}"
        )

        # Проверяем бизнес-результат регистрации
        assert account_created, (
            f"Не удалось создать тестового пользователя. "
            f"Ответ API: {create_data}"
        )

        # Проверяем сообщение API
        assert create_data.get("message") == "User created!", (
            f"Неожиданное сообщение при создании пользователя: "
            f"{create_data.get('message')}"
        )

        # Передаём данные тесту
        yield user_data

    finally:
        # TEARDOWN: удаляем пользователя через API
        if account_created:

            delete_response = api_client.delete(
                DELETE_ACCOUNT,
                data={
                    "email": user_data["email"],
                    "password": user_data["password"]
                }
            )

            # Проверяем HTTP-ответ удаления
            assert delete_response.status_code == 200, (
                f"Не удалось удалить тестового пользователя. "
                f"HTTP-статус: {delete_response.status_code}"
            )

            delete_data = delete_response.json()

            # Проверяем результат удаления
            assert delete_data.get("responseCode") == 200, (
                f"Ошибка при очистке тестовых данных: {delete_data}"
            )

            assert delete_data.get("message") == "Account deleted!", (
                f"Неожиданное сообщение при удалении пользователя: "
                f"{delete_data.get('message')}"
            )


            # Дополнительно проверяем, что пользователь действительно удалён
            with allure.step(
                "Проверяем отсутствие удалённого пользователя через API"
            ):

                verification_response = api_client.get(
                    USER_DETAILS,
                    params={
                        "email": user_data["email"]
                    }
                )

                # Проверяем HTTP-ответ
                assert verification_response.status_code == 200, (
                    f"Не удалось проверить удаление пользователя. "
                    f"HTTP-статус: {verification_response.status_code}"
                )

                verification_data = verification_response.json()

                # Проверяем, что API больше не находит пользователя
                assert verification_data.get("responseCode") == 404, (
                    f"Ожидался бизнес-код 404 после удаления аккаунта. "
                    f"Получен ответ: {verification_data}"
                )

                # Проверяем отсутствие данных пользователя
                assert not verification_data.get("user"), (
                    f"Удалённый пользователь всё ещё доступен через API: "
                    f"{verification_data.get('user')}"
                )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Получаем результат работы остальных реализаций Hook
    outcome = yield
    report = outcome.get_result()

    # Нас интересуют только ошибки внутри тестовой функции
    if report.when != "call" or not report.failed:
        return

    # Получаем Playwright Page из Fixture
    page = item.funcargs.get("page")

    # Если тест не использовал браузерную страницу,
    # создавать screenshot не из чего
    if page is None or page.is_closed():
        return

    try:
        # Создаём папку для скриншотов
        screenshot_dir = (
                Path(__file__).resolve().parents[1]
                / "artifacts"
                / "screenshots"
        )
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Превращаем имя теста в безопасное имя файла
        safe_name = re.sub(
            r"[^A-Za-z0-9_.-]+",
            "_",
            item.nodeid
        )

        screenshot_path = screenshot_dir / f"{safe_name}.png"

        # Делаем screenshot страницы
        screenshot_bytes = page.screenshot(
            full_page=True
        )

        # Сохраняем его на диск
        screenshot_path.write_bytes(screenshot_bytes)

        # Добавляем screenshot в Allure
        allure.attach(
            screenshot_bytes,
            name=f"{item.name} - failure",
            attachment_type=allure.attachment_type.PNG
        )

        print(
            f"\n[SCREENSHOT] Saved: {screenshot_path}"
        )

    except Exception as error:
        # Ошибка создания screenshot не должна
        # скрывать первоначальную причину падения теста
        print(
            f"\n[SCREENSHOT] Capture failed: {error}"
        )
