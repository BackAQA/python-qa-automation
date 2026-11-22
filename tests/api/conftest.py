import pytest


@pytest.fixture
def registered_user(
    api_registered_user: dict[str, str]
) -> dict[str, str]:
    """
    Сохраняет прежнее имя fixture для API-тестов.

    Фактическое создание и удаление пользователя
    выполняется общей fixture api_registered_user.
    """

    return api_registered_user