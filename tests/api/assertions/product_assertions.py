
def assert_product_schema(product: object, index: int) -> None:
    """Validate the structure of one product."""

    assert isinstance(product, dict), (
        f"Product #{index} must be a dictionary"
    )

    # Проверяем наличие обязательных полей
    required_fields = {
        "id",
        "name",
        "price",
        "brand",
        "category"
    }

    missing_fields = required_fields - product.keys()

    assert not missing_fields, (
        f"Product #{index} is missing fields: {missing_fields}"
    )

    # Проверяем ID
    assert type(product["id"]) is int, (
        f"Product #{index}: id must be an integer"
    )

    # Проверяем текстовые поля
    for field in ("name", "price", "brand"):

        value = product[field]

        assert isinstance(value, str) and value.strip(), (
            f"Product #{index}: {field} must be a non-empty string"
        )

    # Проверяем вложенный объект category
    category = product["category"]

    assert isinstance(category, dict), (
        f"Product #{index}: category must be a dictionary"
    )

    assert isinstance(category.get("category"), str), (
        f"Product #{index}: category.category must be a string"
    )

    # Проверяем вложенный объект usertype
    usertype = category.get("usertype")

    assert isinstance(usertype, dict), (
        f"Product #{index}: category.usertype must be a dictionary"
    )

    assert isinstance(usertype.get("usertype"), str), (
        f"Product #{index}: category.usertype.usertype must be a string"
    )


def assert_products_schema(products: object) -> None:
    """Validate the structure of a products list."""

    assert isinstance(products, list), (
        "Products must be a list"
    )

    assert products, (
        "Products list must not be empty"
    )

    for index, product in enumerate(products, start=1):
        assert_product_schema(product, index)
