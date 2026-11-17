
from playwright.sync_api import Page, expect

from pages.product_details_page import ProductDetailsPage


def test_product_details_page_displays_product_information(page: Page) -> None:
    product_page = ProductDetailsPage(page)

    product_page.open(1)

    expect(product_page.product_information).to_be_visible()
    expect(product_page.product_name).to_have_text("Blue Top")
    expect(product_page.price).to_have_text("Rs. 500")

    expect(product_page.category).to_contain_text(
        "Women > Tops"
    )

    expect(product_page.availability).to_contain_text(
        "In Stock"
    )

    expect(product_page.condition).to_contain_text(
        "New"
    )

    expect(product_page.brand).to_contain_text(
        "Polo"
    )


def test_user_can_change_product_quantity(page: Page) -> None:
    product_page = ProductDetailsPage(page)

    product_page.open(1)

    product_page.set_quantity(3)

    expect(product_page.quantity_input).to_have_value("3")


def test_product_quantity_is_one_by_default(page: Page) -> None:
    product_page = ProductDetailsPage(page)

    product_page.open(1)

    expect(product_page.quantity_input).to_have_value("1")
