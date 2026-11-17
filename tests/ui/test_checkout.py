
from playwright.sync_api import Page, expect

from pages.product_details_page import ProductDetailsPage
from pages.cart_page import CartPage


def add_product_to_cart(page: Page) -> None:
    product_page = ProductDetailsPage(page)

    product_page.open(1)
    product_page.set_quantity(3)
    product_page.add_to_cart()

    product_page.cart_modal.should_be_visible()
    product_page.cart_modal.open_cart()


def test_guest_user_sees_login_message_on_checkout(page: Page) -> None:
    # Arrange: добавляем товар в корзину
    add_product_to_cart(page)

    cart_page = CartPage(page)

    # Act: пытаемся оформить заказ
    cart_page.proceed_to_checkout()

    # Assert: появляется модальное окно
    cart_page.checkout_modal.should_be_visible()

    cart_page.checkout_modal.should_have_title("Checkout")

    cart_page.checkout_modal.should_have_login_message()

    expect(
        cart_page.checkout_modal.register_login_link
    ).to_have_attribute("href", "/login")

    expect(
        cart_page.checkout_modal.continue_on_cart_button
    ).to_be_visible()


def test_guest_user_can_continue_on_cart(page: Page) -> None:
    # Arrange
    add_product_to_cart(page)

    cart_page = CartPage(page)

    # Act
    cart_page.proceed_to_checkout()
    cart_page.checkout_modal.should_be_visible()

    cart_page.checkout_modal.continue_on_cart()

    # Assert
    expect(cart_page.checkout_modal.root).to_be_hidden()

    expect(page).to_have_url(
        "https://www.automationexercise.com/view_cart"
    )
