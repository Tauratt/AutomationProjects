import pytest
import pytest_asyncio
from playwright.async_api import async_playwright


"""Фикстуры под каждый браузер"""
@pytest_asyncio.fixture(scope="function")
# @pytest.mark.config({"browser": "chromium"})
async def browser_mobile_chromium():
    """Только Chromium"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    try:
        yield browser, playwright
    finally:
        await browser.close()
        await playwright.stop()



# C указанием браузера - в тесте по типу # @pytest.mark.config({"browser": "chromium", "url": "https://www.saucedemo.com/"})
# ** Можно Использовать в последовательном

@pytest_asyncio.fixture(scope="function")
async def browser_mobile_session(request):
    marker = request.node.get_closest_marker("config")
    config = marker.args[0] if marker else {"browser": "chromium", "url": "https://www.saucedemo.com/"}

    browser_name = config["browser"]

    playwright = await async_playwright().start()
    print(f'\n--Запуск {browser_name} (async)--')
    browser = await getattr(playwright, browser_name).launch(headless=False)

    try:
        yield browser, playwright
    finally:
        print('--Закрытие браузера (async)--')
        await browser.close()
        await playwright.stop()


"""Фикстуры под каждый браузер"""
@pytest_asyncio.fixture(scope="function")
# @pytest.mark.config({"browser": "chromium"})
async def browser_mobile_chromium():
    """Только Chromium"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    try:
        yield browser, playwright
    finally:
        await browser.close()
        await playwright.stop()


@pytest_asyncio.fixture(scope="function")
# @pytest.mark.config({"browser": "firefox"})
async def browser_mobile_firefox():
    """Только Firefox"""
    playwright = await async_playwright().start()
    browser = await playwright.firefox.launch(headless=False)
    try:
        yield browser, playwright
    finally:
        await browser.close()
        await playwright.stop()


@pytest_asyncio.fixture(scope="function")
async def browser_mobile_webkit():
    """Только webkit"""
    playwright = await async_playwright().start()
    browser = await playwright.webkit.launch(headless=False)
    try:
        yield browser, playwright
    finally:
        await browser.close()
        await playwright.stop()


"""Универсальная фикстура"""
@pytest_asyncio.fixture(scope="function")
async def universal_browsers_mobile_sessions():
    """Возвращает все браузеры"""
    playwright = await async_playwright().start()

    chromium = await playwright.chromium.launch(headless=False)
    firefox = await playwright.firefox.launch(headless=False)
    webkit = await playwright.webkit.launch(headless=False)

    try:
        yield {
            "chromium": chromium,
            "firefox": firefox,
            "webkit":webkit
        }, playwright
    finally:
        await chromium.close()
        await firefox.close()
        await playwright.stop()



# Использование
# async def test_parallel(browsers):
#     async def chrome_task():
#         # используем browsers["chromium"]
#         pass
#
#     async def firefox_task():
#         # используем browsers["firefox"]
#         pass
#
#     await asyncio.gather(chrome_task(), firefox_task())