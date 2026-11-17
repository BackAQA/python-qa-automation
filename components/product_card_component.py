from playwright.sync_api import Locator


class ProductCardComponent:

    def __init__(self, root: Locator) -> None:

        self.root = root

        # Main product information section
        self.product_info = self.root.locator(
            ".productinfo"
        )

        # Product name
        self.name = self.product_info.locator("p")

        # Product price
        self.price = self.product_info.locator("h2")

        # Product image
        self.image = self.product_info.locator("img")

        # Product details link
        self.view_product_link = self.root.get_by_role(
            "link",
            name="View Product"
        )

    def get_name(self) -> str:
        return self.name.inner_text().strip()

    def get_price(self) -> str:
        return self.price.inner_text().strip()

    def get_image_src(self) -> str | None:
        return self.image.get_attribute("src")

    def open_details(self) -> None:
        self.view_product_link.click()