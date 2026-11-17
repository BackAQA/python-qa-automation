from playwright.sync_api import Page


class HeaderComponent:

    def __init__(self, page: Page) -> None:
        self.page = page

        self.products_link = self.page.get_by_role(
            "link",
            name="Products"
        )

        self.cart_link = self.page.get_by_role(
            "link",
            name="Cart"
        )

    def click_products(self) -> None:
        self.products_link.click()

    def click_cart(self) -> None:
        self.cart_link.click()