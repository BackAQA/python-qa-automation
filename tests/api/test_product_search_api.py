
import pytest

from api.endpoints.products import SEARCH_PRODUCTS
from tests.api.assertions.product_assertions import assert_products_schema


def get_searchable_product_text(product: dict) -> str:

    category = product["category"]
    usertype = category["usertype"]

    searchable_values = [
        product["name"],
        product["brand"],
        category["category"],
        usertype["usertype"]
    ]

    return " ".join(searchable_values).casefold()


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize(
    "search_term",
    ["top", "tshirt", "jean"],
    ids=["tops", "tshirts", "jeans"]
)
def test_search_products(api_client, search_term):

    response = api_client.post(
        SEARCH_PRODUCTS,
        data={"search_product": search_term}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("responseCode") == 200

    products = response_data.get("products")

    # Проверяем структуру всех найденных товаров
    assert_products_schema(products)

    # Проверяем соответствие результатов поисковому запросу
    for index, product in enumerate(products, start=1):

        searchable_text = get_searchable_product_text(product)

        assert search_term.casefold() in searchable_text, (
            f"Product #{index} does not match search term "
            f"'{search_term}'. "
            f"Product data: {searchable_text}"
        )


@pytest.mark.api
@pytest.mark.regression
def test_search_products_without_search_term(api_client):

    response = api_client.post(
        SEARCH_PRODUCTS,
        data={}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("responseCode") == 400

    assert response_data.get("message") == (
        "Bad request, search_product parameter is missing in POST request."
    )
