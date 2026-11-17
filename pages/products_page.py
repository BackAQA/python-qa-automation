from playwright.sync_api import Page

from components.product_card_component import ProductCardComponent
from pages.base_page import BasePage


class ProductsPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.page_heading = self.page.get_by_role(
            "heading",
            name="All Products",
            exact=True
        )

        self.search_input = self.page.get_by_placeholder(
            "Search Product"
        )

        self.product_view_links = self.page.get_by_role(
            "link",
            name="View Product"
        )

        self.product_cards = self.page.locator(
            ".product-image-wrapper"
        )

    def open(self) -> None:
        self.navigate("/products")

    def get_product_card(
        self,
        product_name: str
    ) -> ProductCardComponent:

        card = self.product_cards.filter(
            has_text=product_name
        )

        return ProductCardComponent(card)