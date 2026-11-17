
from playwright.sync_api import Page

from pages.base_page import BasePage
from components.cart_item_component import CartItemComponent
from components.checkout_modal_component import CheckoutModalComponent


class CartPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.cart_table = self.page.locator(
            "#cart_info_table"
        )

        self.product_rows = self.cart_table.locator(
            "tbody tr[id^='product-']"
        )

        self.checkout_link = self.page.locator("a.check_out")

        self.checkout_modal = CheckoutModalComponent(
            self.page.locator("#checkoutModal")
        )

    def open(self) -> None:
        self.navigate("/view_cart")

    def get_item(self, product_id: int) -> CartItemComponent:
        row = self.cart_table.locator(
            f"#product-{product_id}"
        )

        return CartItemComponent(row)

    def proceed_to_checkout(self) -> None:
        self.checkout_link.click()

    def should_show_checkout_modal(self) -> None:
        self.checkout_modal.should_be_visible()