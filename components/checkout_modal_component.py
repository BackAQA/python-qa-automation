
from playwright.sync_api import Locator, expect


class CheckoutModalComponent:

    def __init__(self, root: Locator) -> None:
        self.root = root

        self.title = self.root.locator(".modal-title")

        self.message = self.root.locator(".modal-body")

        self.register_login_link = self.root.get_by_role(
            "link",
            name="Register / Login",
            exact=True
        )

        self.continue_on_cart_button = self.root.get_by_role(
            "button",
            name="Continue On Cart",
            exact=True
        )

    def should_be_visible(self) -> None:
        expect(self.root).to_be_visible()

    def should_have_title(self, title: str) -> None:
        expect(self.title).to_have_text(title)

    def should_have_login_message(self) -> None:
        expect(self.message).to_contain_text(
            "Register / Login account to proceed on checkout."
        )

    def open_login_page(self) -> None:
        self.register_login_link.click()

    def continue_on_cart(self) -> None:
        self.continue_on_cart_button.click()
