import pytest

from api.endpoints.users import VERIFY_LOGIN, USER_DETAILS, UPDATE_ACCOUNT


@pytest.mark.api
@pytest.mark.regression
def test_registered_user_can_login(api_client, registered_user):
    """Проверка авторизации зарегистрированного пользователя."""

    response = api_client.post(
        VERIFY_LOGIN,
        data={
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
    )

    # Проверяем HTTP-статус
    assert response.status_code == 200, (
        f"Ожидался HTTP-статус 200, получен {response.status_code}."
    )

    response_data = response.json()

    # Проверяем результат авторизации
    assert response_data.get("responseCode") == 200, (
        f"Пользователь не прошёл авторизацию. Ответ API: {response_data}"
    )

    # Проверяем сообщение API
    assert response_data.get("message") == "User exists!", (
        f"Неожиданное сообщение при авторизации: "
        f"{response_data.get('message')}"
    )

@pytest.mark.api
@pytest.mark.regression
def test_get_user_details_by_email(api_client, registered_user):
    """Проверка получения профиля пользователя по электронной почте."""

    response = api_client.get(
        USER_DETAILS,
        params={
            "email": registered_user["email"]
        }
    )

    # Проверяем HTTP-статус
    assert response.status_code == 200, (
        f"Ожидался HTTP-статус 200, получен {response.status_code}."
    )

    response_data = response.json()

    # Проверяем результат операции
    assert response_data.get("responseCode") == 200, (
        f"Не удалось получить профиль пользователя: {response_data}"
    )

    # Получаем объект пользователя
    user = response_data.get("user")

    assert isinstance(user, dict), (
        "В ответе API отсутствует объект пользователя."
    )

    # Проверяем данные найденного пользователя
    assert user.get("email") == registered_user["email"], (
        "Электронная почта в ответе не совпадает с запрошенной."
    )

    assert user.get("name") == registered_user["name"], (
        "Имя пользователя в ответе не совпадает с зарегистрированным."
    )

@pytest.mark.api
@pytest.mark.regression
def test_update_user_account(api_client, registered_user):
    """Проверка изменения данных зарегистрированного пользователя."""

    # Копируем первоначальные данные пользователя
    updated_user = registered_user.copy()

    # Меняем имя пользователя
    updated_user["name"] = "QA Automation Updated"

    response = api_client.put(
        UPDATE_ACCOUNT,
        data=updated_user
    )

    # Проверяем HTTP-статус
    assert response.status_code == 200, (
        f"Ожидался HTTP-статус 200, получен {response.status_code}."
    )

    response_data = response.json()

    # Проверяем успешное обновление
    assert response_data.get("responseCode") == 200, (
        f"Не удалось обновить пользователя: {response_data}"
    )

    assert response_data.get("message") == "User updated!", (
        f"Неожиданное сообщение при обновлении: "
        f"{response_data.get('message')}"
    )

    # Повторно запрашиваем профиль пользователя
    details_response = api_client.get(
        USER_DETAILS,
        params={
            "email": registered_user["email"]
        }
    )

    assert details_response.status_code == 200, (
        f"Не удалось получить обновлённый профиль. "
        f"HTTP-статус: {details_response.status_code}"
    )

    details_data = details_response.json()

    assert details_data.get("responseCode") == 200, (
        f"Не удалось получить данные после обновления: {details_data}"
    )

    updated_profile = details_data.get("user")

    assert isinstance(updated_profile, dict), (
        "В ответе отсутствует объект обновлённого пользователя."
    )

    assert updated_profile.get("name") == updated_user["name"], (
        "Имя пользователя не изменилось после PUT-запроса."
    )