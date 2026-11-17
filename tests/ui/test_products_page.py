from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage
import re

def test_products_page_displays_products(page: Page) -> None:

    products_page = ProductsPage(page)

    products_page.open()

    print(
        "Количество ссылок View Product:",
        products_page.product_view_links.count()
    )

    expect(
        products_page.page_heading
    ).to_be_visible()

    expect(
        products_page.search_input
    ).to_be_visible()

    expect(
        products_page.product_view_links.first
    ).to_be_visible()

def test_products_page_displays_products(page: Page) -> None:

    products_page = ProductsPage(page)

    products_page.open()

    expect(
        products_page.page_heading
    ).to_be_visible()

    expect(
        products_page.search_input
    ).to_be_visible()

    expect(
        products_page.product_view_links.first
    ).to_be_visible()


def test_user_can_find_product_by_name(page: Page) -> None:

    products_page = ProductsPage(page)

    products_page.open()

    blue_top = products_page.get_product_card("Blue Top")

    expect(blue_top.root).to_have_count(1)

    expect(blue_top.name).to_have_text("Blue Top")

    expect(blue_top.price).to_have_text("Rs. 500")

    expect(blue_top.image).to_have_attribute(
        "src",
        "/get_product_picture/1"
    )

    expect(blue_top.view_product_link).to_have_attribute(
        "href",
        "/product_details/1"
    )

def test_user_can_open_specific_product(page: Page) -> None:

    products_page = ProductsPage(page)

    products_page.open()

    blue_top = products_page.get_product_card("Blue Top")

    expect(blue_top.root).to_have_count(1)

    blue_top.open_details()

    expect(page).to_have_url(
        re.compile(r"/product_details/1/?$")
    )