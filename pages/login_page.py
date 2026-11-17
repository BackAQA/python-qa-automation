
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Login form
        self.login_form = self.page.locator(
            "form[action='/login']"
        )

        self.login_email_input = self.login_form.get_by_placeholder(
            "Email Address",
            exact=True
        )

        self.login_password_input = self.login_form.get_by_placeholder(
            "Password",
            exact=True
        )

        self.login_button = self.login_form.get_by_role(
            "button",
            name="Login",
            exact=True
        )

        # Signup form
        self.signup_form = self.page.locator(
            "form[action='/signup']"
        )

        self.signup_name_input = self.signup_form.get_by_placeholder(
            "Name",
            exact=True
        )

        self.signup_email_input = self.signup_form.get_by_placeholder(
            "Email Address",
            exact=True
        )

        self.signup_button = self.signup_form.get_by_role(
            "button",
            name="Signup",
            exact=True
        )

        self.login_error_message = self.login_form.get_by_text(
            "Your email or password is incorrect!",
            exact=True
        )

        # Authenticated user elements
        self.logged_in_message = self.page.get_by_text(
            "Logged in as",
            exact=False
        )

        self.logout_link = self.page.locator('a[href="/logout"]')

        self.delete_account_link = self.page.locator('a[href="/delete_account"]')

    def open(self) -> None:
        self.navigate("/login")

    def login(self, email: str, password: str) -> None:
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_button.click()

    def signup(self, name: str, email: str) -> None:
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()

    def should_show_login_error(self) -> None:
        expect(self.login_error_message).to_be_visible()

        expect(self.login_error_message).to_have_text(
            "Your email or password is incorrect!"
        )

    def should_be_logged_in_as(self, name: str) -> None:
        expect(self.logged_in_message).to_be_visible()

        expect(self.logged_in_message).to_contain_text(name)

    def logout(self) -> None:
        self.logout_link.click()

    def delete_account(self) -> None:
        self.delete_account_link.click()