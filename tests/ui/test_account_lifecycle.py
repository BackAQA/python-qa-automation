
import re

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_user_is_logged_in_after_registration(page: Page, registered_user: dict[str, str]) -> None:

    login_page = LoginPage(page)

    # Verify authenticated user
    login_page.should_be_logged_in_as(
        registered_user["name"]
    )

    expect(login_page.logout_link).to_be_visible()

    expect(login_page.delete_account_link).to_be_visible()


def test_user_can_login_with_valid_credentials(page: Page, registered_user: dict[str, str]) -> None:

    login_page = LoginPage(page)

    # First, log out
    login_page.logout()

    expect(page).to_have_url(
        re.compile(r"/login/?$")
    )

    # Login with registered user credentials
    login_page.login(
        email=registered_user["email"],
        password=registered_user["password"]
    )

    # Verify successful authentication
    login_page.should_be_logged_in_as(
        registered_user["name"]
    )


def test_user_can_logout(page: Page, registered_user: dict[str, str]) -> None:

    login_page = LoginPage(page)

    # Logout
    login_page.logout()

    # Verify redirection to login page
    expect(page).to_have_url(
        re.compile(r"/login/?$")
    )

    # Verify authenticated elements are absent
    expect(login_page.logout_link).to_have_count(0)

    expect(login_page.logged_in_message).to_have_count(0)
