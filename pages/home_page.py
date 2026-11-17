from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.products_page import ProductsPage


class HomePage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate("/")

    def open_products(self) -> ProductsPage:
        self.header.click_products()
        self.page.wait_for_url("**/products")
        self.page.wait_for_load_state("domcontentloaded")
        return ProductsPage(self.page)