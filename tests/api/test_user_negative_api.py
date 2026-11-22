
import pytest

from api.endpoints.users import CREATE_ACCOUNT, USER_DETAILS


@pytest.mark.api
@pytest.mark.regression
def test_register_user_with_existing_email(api_client, registered_user):
    """Проверка запрета повторной регистрации с существующей электронной почтой."""

    # Получаем первоначальные данные зарегистрированного пользователя
    original_response = api_client.get(
        USER_DETAILS,
        params={"email": registered_user["email"]}
    )

    assert original_response.status_code == 200, (
        f"Не удалось получить первоначальный профиль. "
        f"HTTP-статус: {original_response.status_code}"
    )

    original_data = original_response.json()

    assert original_data.get("responseCode") == 200, (
        f"Не удалось получить первоначальные данные пользователя: "
        f"{original_data}"
    )

    original_user = original_data.get("user")

    assert isinstance(original_user, dict), (
        "В ответе API отсутствует первоначальный профиль пользователя."
    )

    # Подготавливаем повторную регистрацию с тем же email
    duplicate_user = registered_user.copy()

    duplicate_user["name"] = "Duplicate QA User"
    duplicate_user["firstname"] = "Duplicate"
    duplicate_user["lastname"] = "Attempt"

    # Отправляем запрос на повторную регистрацию
    duplicate_response = api_client.post(
        CREATE_ACCOUNT,
        data=duplicate_user
    )

    assert duplicate_response.status_code == 200, (
        f"Ожидался HTTP-статус 200, "
        f"получен {duplicate_response.status_code}."
    )

    duplicate_data = duplicate_response.json()

    # Проверяем, что API отклонило повторную регистрацию
    assert duplicate_data.get("responseCode") == 400, (
        f"Ожидался отказ в повторной регистрации. "
        f"Ответ API: {duplicate_data}"
    )

    assert duplicate_data.get("message") == "Email already exists!", (
        f"Неожиданное сообщение API при повторной регистрации: "
        f"{duplicate_data.get('message')}"
    )

    # Повторно получаем профиль после неудачной регистрации
    actual_response = api_client.get(
        USER_DETAILS,
        params={"email": registered_user["email"]}
    )

    assert actual_response.status_code == 200, (
        f"Не удалось повторно получить профиль. "
        f"HTTP-статус: {actual_response.status_code}"
    )

    actual_data = actual_response.json()

    assert actual_data.get("responseCode") == 200, (
        f"Профиль пользователя недоступен после повторной регистрации: "
        f"{actual_data}"
    )

    actual_user = actual_data.get("user")

    assert actual_user == original_user, (
        "Данные существующего пользователя изменились "
        "после отклонённой повторной регистрации."
    )
