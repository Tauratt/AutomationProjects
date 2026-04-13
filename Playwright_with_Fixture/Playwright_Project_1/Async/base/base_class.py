import datetime
import os

import allure
from datetime import datetime
from Playwright_with_Fixture.Playwright_Project_1.Async.config import SCREENSHOT_DIR
from Playwright_with_Fixture.Playwright_Project_1.Async.utilities.utils import (
    log_message,
    error
)
from Playwright_with_Fixture.Playwright_Project_1.Async.helper_func.error_class import LocatorNotFoundError
from Playwright_with_Fixture.Playwright_Project_1.Async.utilities.utils import error


# await self.page.locator(login_button).click() нужен не потому, что locator «асинхронный»,
# а потому что метод click() в async‑API возвращает корутину.
# В async‑Playwright все «действия с браузером» — это асинхронные операции:
# запуск браузера;
# переход по URL;
# поиск элемента и клик;
# ввод текста;
# ожидания и проверки.

# Каждый такой вызов в async‑версии возвращает объект‑корутину, который нужно дождаться,
# чтобы операция реально выполнилась. Если писать без await:

# self.page.locator(login_button).click()  # ← в async-функции это просто создаст корутину и
# ничего не сделает


class Settings:
    def __init__(self, page, expect):
        self.page = page
        self.expect = expect


    async def check_expect_exists(self, locator, *, timeout: int = 5000, name: str = "", msg: str | None = None):
        """
        Web-first проверка “элемент существует” (count != 0). Множественное, например > 0

        Ждёт (с ретраями до `timeout`), что `locator` будет матчиться минимум на 1 элемент.
        Если не дождались — бросает LocatorNotFoundError с кастомным `msg` или дефолтным.
        """
        try:
            await self.expect(locator).not_to_have_count(0, timeout=timeout)
        except AssertionError as e:
            prefix = f"[{name}] " if name else ""
            raise LocatorNotFoundError(
                msg or f"{prefix}Element not found: locator={locator}"
            ) from e


    async def check_expect_count(self, locator, expected: int, *, timeout: int = 5000, name: str = ""):
        """
        Web-first проверка Точного количества элементов по локатору.

        Ждёт (с ретраями до `timeout`), что `locator` будет матчиться ровно на `expected` элементов.
        Удобно использовать перед действиями (click/fill/read), чтобы:
        - стабилизировать тесты при асинхронной подгрузке/рендере UI;
        - явно проваливать тест, если локатор слишком широкий (нашёл >1) или не нашёл ничего (0).

        Параметры:
        - locator: Playwright Locator (например, `page.locator("...")`).
        - expected: ожидаемое точное количество элементов.
        - timeout: максимальное время ожидания в миллисекундах.
        - name: опциональный префикс/название шага для более читаемого сообщения об ошибке.

        Исключения:
        - Если условие не выполнено за `timeout`, Playwright выбрасывает AssertionError.
          Метод перехватывает его и выбрасывает твою `locator_not_found_error(...)`
          с понятным сообщением, сохраняя исходную причину через `raise ... from e`.
        """
        try:
            await self.expect(locator).to_have_count(expected, timeout=timeout)
        except AssertionError as e:
            prefix = f"[{name}] " if name else ""
            raise LocatorNotFoundError(
                f'{prefix}Expected count={expected}, but not met. locator={locator}'
            ) from e


    # =================Не используется===================
    # def locator_not_found_error(self, locator: str):
    #     """Кастомный вывод ошибки"""
    #     error = Exception(
    #         f'Locator "{locator}" was not found'
    #     )
    #     error.__class__.__name__ = "LocatorNotFoundError"
    #     return error


    async def get_current_url(self):
        """Логирует и возвращает текущий URL страницы."""
        try:
            current_url = self.page.url
            log_message(f'🌐 Current URL: {current_url}')
            return current_url
        except Exception as e:
            error(f"Ошибка при получении текущего URL: {e}")
            return None


    async def check_assert_url(self, checker_url: str) -> str:
        current_url = self.get_current_url()
        if current_url == checker_url:
            return 'GOOD ✅'
        else:
            return 'BAD ❌'


    async def get_screenshot(self, name_page):
        """Создание скриншота"""


        now_date = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
        name_screenshot = f"{name_page} {now_date}.png"

        screenshot_path = os.path.join(SCREENSHOT_DIR, name_screenshot)

        await self.page.screenshot(path=screenshot_path)
        log_message("Скриншот выполнен")


