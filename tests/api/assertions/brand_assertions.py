
def assert_brand_schema(brand: object, index: int) -> None:
    """Validate the structure of one brand."""

    assert isinstance(brand, dict), (
        f"Brand #{index} must be a dictionary"
    )

    required_fields = {"id", "brand"}

    missing_fields = required_fields - brand.keys()

    assert not missing_fields, (
        f"Brand #{index} is missing fields: {missing_fields}"
    )

    assert type(brand["id"]) is int, (
        f"Brand #{index}: id must be an integer"
    )

    assert isinstance(brand["brand"], str) and brand["brand"].strip(), (
        f"Brand #{index}: brand name must be a non-empty string"
    )


def assert_brands_schema(brands: object) -> None:
    """Validate the structure of a brands list."""

    assert isinstance(brands, list), (
        "Brands must be a list"
    )

    assert brands, (
        "Brands list must not be empty"
    )

    for index, brand in enumerate(brands, start=1):
        assert_brand_schema(brand, index)
