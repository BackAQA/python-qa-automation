
import pytest

from api.endpoints.brands import BRANDS_LIST
from tests.api.assertions.brand_assertions import assert_brands_schema


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_brands(api_client):

    response = api_client.get(BRANDS_LIST)

    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data, dict)
    assert response_data.get("responseCode") == 200

    brands = response_data.get("brands")

    assert_brands_schema(brands)
