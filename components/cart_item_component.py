
from playwright.sync_api import Locator


class CartItemComponent:

    def __init__(self, root: Locator) -> None:
        self.root = root

        self.name = self.root.locator(
            ".cart_description h4 a"
        )

        self.category = self.root.locator(
            ".cart_description p"
        )

        self.price = self.root.locator(
            ".cart_price p"
        )

        self.quantity = self.root.locator(
            ".cart_quantity button"
        )

        self.total = self.root.locator(
            ".cart_total_price"
        )

        self.delete_button = self.root.locator(
            ".cart_quantity_delete"
        )

    def get_name(self) -> str:
        return self.name.inner_text().strip()

    def get_category(self) -> str:
        return self.category.inner_text().strip()

    def get_price(self) -> str:
        return self.price.inner_text().strip()

    def get_quantity(self) -> str:
        return self.quantity.inner_text().strip()

    def get_total(self) -> str:
        return self.total.inner_text().strip()

    def remove(self) -> None:
        self.delete_button.click()
