import re

from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_user_can_open_products_page(page: Page) -> None:

    home_page = HomePage(page)

    home_page.open()

    expect(home_page.header.products_link).to_be_visible()

    products_page = home_page.open_products()

    expect(page).to_have_url(
        re.compile(r"/products/?$")
    )

    expect(products_page.page_heading).to_be_visible()

    expect(products_page.header.products_link).to_be_visible()