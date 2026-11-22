
import pytest

from api.endpoints.products import PRODUCTS_LIST
from tests.api.assertions.product_assertions import assert_products_schema


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_products(api_client):

    response = api_client.get(PRODUCTS_LIST)

    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data, dict)
    assert response_data.get("responseCode") == 200

    products = response_data.get("products")

    assert_products_schema(products)
