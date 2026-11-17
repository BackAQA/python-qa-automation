from playwright.sync_api import Page, expect
import pytest

from pages.product_details_page import ProductDetailsPage
from pages.cart_page import CartPage


pytestmark = [
    pytest.mark.ui,
    pytest.mark.regression
]

def add_product_to_cart(page: Page, quantity: int = 3) -> None:
    product_page = ProductDetailsPage(page)

    product_page.open(1)
    product_page.set_quantity(quantity)
    product_page.add_to_cart()

    product_page.cart_modal.should_be_visible()
    product_page.cart_modal.open_cart()

@pytest.mark.smoke
def test_cart_displays_added_product(page: Page) -> None:
    add_product_to_cart(page, quantity=3)

    cart_page = CartPage(page)
    cart_item = cart_page.get_item(1)

    expect(cart_page.cart_table).to_be_visible()
    expect(cart_item.root).to_be_visible()

    expect(cart_item.name).to_have_text("Blue Top")
    expect(cart_item.category).to_have_text("Women > Tops")
    expect(cart_item.price).to_have_text("Rs. 500")
    expect(cart_item.quantity).to_have_text("3")
    expect(cart_item.total).to_have_text("Rs. 1500")

    expect(cart_page.product_rows).to_have_count(1)


def test_user_can_remove_product_from_cart(page: Page) -> None:
    add_product_to_cart(page, quantity=1)

    cart_page = CartPage(page)
    cart_item = cart_page.get_item(1)

    expect(cart_item.root).to_be_visible()

    cart_item.remove()

    expect(cart_item.root).to_be_hidden()
    expect(cart_page.product_rows).to_have_count(0)


@pytest.mark.parametrize(
    "quantity",
    [
        pytest.param(1, id="quantity-1"),
        pytest.param(2, id="quantity-2"),
        pytest.param(3, id="quantity-3"),
        pytest.param(5, id="quantity-5"),
    ]
)
def test_cart_calculates_total_based_on_quantity(page: Page, quantity: int) -> None:

    # Arrange: добавляем товар с заданным количеством
    add_product_to_cart(
        page,
        quantity=quantity
    )

    cart_page = CartPage(page)
    cart_item = cart_page.get_item(1)

    # Act: получаем ожидаемую общую стоимость
    expected_total = f"Rs. {500 * quantity}"

    # Assert: проверяем количество
    expect(cart_item.quantity).to_have_text(
        str(quantity)
    )

    # Проверяем общую стоимость
    expect(cart_item.total).to_have_text(
        expected_total
    )
