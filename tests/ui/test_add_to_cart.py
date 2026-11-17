
import re

from playwright.sync_api import Page, expect

from pages.product_details_page import ProductDetailsPage


def test_user_can_add_product_to_cart(
    page: Page
) -> None:
    product_page = ProductDetailsPage(page)

    product_page.open(1)
    product_page.set_quantity(3)
    product_page.add_to_cart()

    product_page.cart_modal.should_be_visible()

    product_page.cart_modal.should_have_title("Added!")

    product_page.cart_modal.should_have_success_message()

    expect(
        product_page.cart_modal.view_cart_link
    ).to_have_attribute("href", "/view_cart")

    expect(
        product_page.cart_modal.continue_shopping_button
    ).to_be_visible()


def test_user_can_open_cart_after_adding_product(
    page: Page
) -> None:
    product_page = ProductDetailsPage(page)

    product_page.open(1)
    product_page.add_to_cart()

    product_page.cart_modal.should_be_visible()

    product_page.cart_modal.open_cart()

    expect(page).to_have_url(
        re.compile(r"/view_cart/?$")
    )


def test_user_can_continue_shopping_after_adding_product(
    page: Page
) -> None:
    product_page = ProductDetailsPage(page)

    product_page.open(1)
    product_page.add_to_cart()

    product_page.cart_modal.should_be_visible()

    product_page.cart_modal.continue_shopping()

    expect(
        product_page.cart_modal.root
    ).to_be_hidden()
