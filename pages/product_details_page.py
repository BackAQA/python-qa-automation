import re

from playwright.sync_api import Page, Locator

from pages.base_page import BasePage
from components.cart_modal_component import CartModalComponent

class ProductDetailsPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.product_information = self.page.locator(
            ".product-information"
        )

        self.product_name = self.product_information.locator("h2")

        self.category = self.product_information.locator(
            "p"
        ).filter(has_text="Category:")

        self.price = page.locator(".product-information").get_by_text(re.compile(r"^Rs\. \d+$"))

        self.quantity_input = self.product_information.locator(
            "#quantity"
        )

        self.add_to_cart_button = self.product_information.get_by_role(
            "button",
            name="Add to cart"
        )

        self.availability = self.product_information.locator(
            "p"
        ).filter(has_text="Availability:")

        self.condition = self.product_information.locator(
            "p"
        ).filter(has_text="Condition:")

        self.brand = self.product_information.locator(
            "p"
        ).filter(has_text="Brand:")

        self.cart_modal = CartModalComponent(
            self.page.locator("#cartModal")
        )

    def open(self, product_id: int) -> None:
        self.navigate(f"/product_details/{product_id}")

    def get_product_name(self) -> str:
        return self.product_name.inner_text().strip()

    def get_price(self) -> str:
        return self.price.inner_text().strip()

    def set_quantity(self, quantity: int) -> None:
        self.quantity_input.fill(str(quantity))

    def get_quantity(self) -> str:
        return self.quantity_input.input_value()

    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()
