
from typing import Any
from urllib.parse import urlsplit

import requests

from utils.logger import logger


class ApiClient:

    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        # История запросов текущего клиента
        self.request_history: list[dict[str, Any]] = []

    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any
    ) -> requests.Response:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        endpoint_path = urlsplit(url).path

        kwargs.setdefault("timeout", self.timeout)

        logger.info(
            "Отправка %s-запроса: %s",
            method.upper(),
            endpoint_path
        )

        try:
            response = self.session.request(
                method=method,
                url=url,
                **kwargs
            )

        except requests.RequestException as error:

            # Сохраняем информацию об ошибке без конфиденциальных данных
            self.request_history.append({
                "метод": method.upper(),
                "адрес": endpoint_path,
                "результат": "Ошибка",
                "тип_ошибки": type(error).__name__
            })

            logger.exception(
                "Ошибка при выполнении %s-запроса: %s",
                method.upper(),
                endpoint_path
            )

            raise

        # Получаем время обработки запроса
        response_time = response.elapsed.total_seconds()

        # Сохраняем информацию об успешном получении HTTP-ответа
        self.request_history.append({
            "метод": method.upper(),
            "адрес": endpoint_path,
            "HTTP-статус": response.status_code,
            "время_ответа_сек": round(response_time, 3)
        })

        if response.status_code >= 400:
            logger.warning(
                "Получен HTTP %s: %s, время: %.3f сек.",
                response.status_code,
                endpoint_path,
                response_time
            )
        else:
            logger.info(
                "Получен HTTP %s: %s, время: %.3f сек.",
                response.status_code,
                endpoint_path,
                response_time
            )

        return response

    def get(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)

    def close(self) -> None:
        self.session.close()
