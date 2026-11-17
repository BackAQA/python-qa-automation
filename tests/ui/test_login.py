
import re
import pytest

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_login_form_is_displayed(page: Page) -> None:
    login_page = LoginPage(page)

    login_page.open()

    expect(login_page.login_form).to_be_visible()

    expect(login_page.login_email_input).to_be_visible()

    expect(login_page.login_password_input).to_be_visible()

    expect(login_page.login_button).to_be_visible()


def test_signup_form_is_displayed(page: Page) -> None:
    login_page = LoginPage(page)

    login_page.open()

    expect(login_page.signup_form).to_be_visible()

    expect(login_page.signup_name_input).to_be_visible()

    expect(login_page.signup_email_input).to_be_visible()

    expect(login_page.signup_button).to_be_visible()


@pytest.mark.parametrize(
    ("email", "password"),
    [
        pytest.param(
            "qa.unknown.one@example.invalid",
            "WrongPassword123!",
            id="unknown-user-one"
        ),
        pytest.param(
            "qa.unknown.two@example.invalid",
            "IncorrectPassword456!",
            id="unknown-user-two"
        ),
    ]
)
def test_login_shows_error_for_invalid_credentials(page: Page, email: str, password: str) -> None:

    # Arrange
    login_page = LoginPage(page)
    login_page.open()

    # Act
    login_page.login(
        email=email,
        password=password
    )

    # Assert
    login_page.should_show_login_error()

    expect(page).to_have_url(
        re.compile(r"/login/?$")
    )
