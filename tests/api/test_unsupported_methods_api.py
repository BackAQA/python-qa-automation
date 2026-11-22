
import pytest

from api.endpoints.products import PRODUCTS_LIST
from api.endpoints.brands import BRANDS_LIST


@pytest.mark.api
@pytest.mark.regression
def test_post_products_list_method_not_supported(api_client):

    response = api_client.post(PRODUCTS_LIST)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("responseCode") == 405

    assert response_data.get("message") == (
        "This request method is not supported."
    )


@pytest.mark.api
@pytest.mark.regression
def test_put_brands_list_method_not_supported(api_client):

    response = api_client.put(BRANDS_LIST)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("responseCode") == 405

    assert response_data.get("message") == (
        "This request method is not supported."
    )
