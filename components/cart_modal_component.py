
from playwright.sync_api import Locator, expect


class CartModalComponent:

    def __init__(self, root: Locator) -> None:
        self.root = root

        self.title = self.root.locator(".modal-title")

        self.message = self.root.locator(
            ".modal-body"
        )

        self.view_cart_link = self.root.get_by_role(
            "link",
            name="View Cart",
            exact=True
        )

        self.continue_shopping_button = self.root.get_by_role(
            "button",
            name="Continue Shopping",
            exact=True
        )

    def should_be_visible(self) -> None:
        expect(self.root).to_be_visible(timeout=15_000)

    def should_have_title(self, title: str) -> None:
        expect(self.title).to_have_text(title)

    def should_have_success_message(self) -> None:
        expect(self.message).to_contain_text(
            "Your product has been added to cart."
        )

    def open_cart(self) -> None:
        self.view_cart_link.click()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()
