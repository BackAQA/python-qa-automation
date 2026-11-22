
import pytest

from api.endpoints.users import VERIFY_LOGIN


@pytest.mark.api
@pytest.mark.regression
def test_verify_login_without_email(api_client):
    """Проверка ошибки авторизации при отсутствии электронной почты."""

    response = api_client.post(
        VERIFY_LOGIN,
        data={"password": "ТестовыйПароль123!"}
    )

    # Проверяем HTTP-статус ответа
    assert response.status_code == 200, (
        f"Ожидался HTTP-статус 200, "
        f"получен {response.status_code}. "
        f"Ответ сервера: {response.text}"
    )

    response_data = response.json()

    assert isinstance(response_data, dict), (
        "Ответ сервера должен быть JSON-объектом."
    )

    # Проверяем внутренний код ошибки API
    assert response_data.get("responseCode") == 400, (
        "При отсутствии электронной почты "
        "API должен вернуть код ошибки 400."
    )

    # Проверяем оригинальное сообщение внешнего API
    assert response_data.get("message") == (
        "Bad request, email or password parameter is missing in POST request."
    ), (
        "API вернул неожиданное сообщение об отсутствии обязательного параметра."
    )


@pytest.mark.api
@pytest.mark.regression
def test_verify_login_with_invalid_credentials(api_client):
    """Проверка отказа в авторизации с несуществующими учётными данными."""

    response = api_client.post(
        VERIFY_LOGIN,
        data={
            "email": "qa-user-not-found@example.invalid",
            "password": "НеверныйПароль123!"
        }
    )

    # Проверяем HTTP-статус ответа
    assert response.status_code == 200, (
        f"Ожидался HTTP-статус 200, "
        f"получен {response.status_code}. "
        f"Ответ сервера: {response.text}"
    )

    response_data = response.json()

    assert isinstance(response_data, dict), (
        "Ответ сервера должен быть JSON-объектом."
    )

    # Проверяем внутренний код ошибки API
    assert response_data.get("responseCode") == 404, (
        "При неверных учётных данных API должен вернуть код 404."
    )

    # Проверяем оригинальное сообщение внешнего API
    assert response_data.get("message") == "User not found!", (
        "API вернул неожиданное сообщение при отсутствии пользователя."
    )
