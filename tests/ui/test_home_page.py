from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_home_page_is_displayed(page: Page) -> None:

    home_page = HomePage(page)

    home_page.open()

    expect(page).to_have_title("Automation Exercise")

    expect(home_page.header.products_link).to_be_visible()

    expect(home_page.header.products_link).to_have_count(1)