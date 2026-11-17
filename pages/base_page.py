from playwright.sync_api import Page

from components.header_component import HeaderComponent


class BasePage:

    def __init__(self, page: Page) -> None:
        self.page = page

        self.header = HeaderComponent(page)

    def navigate(self, path: str = "/") -> None:
        self.page.goto(
            path,
            wait_until="domcontentloaded",   # не ждём картинки/рекламу/трекеры
            timeout=60_000                   # запас на медленный ответ сервера
        )