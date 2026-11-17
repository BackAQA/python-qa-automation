
from typing import Iterator
from uuid import uuid4

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.signup_page import SignupPage
import re
from pathlib import Path
import allure

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
