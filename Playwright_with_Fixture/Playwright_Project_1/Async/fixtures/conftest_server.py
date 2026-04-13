import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

"""Фикстуры для запуска в Docker"""

# C указанием браузера - в тесте по типу # @pytest.mark.config({"browser": "chromium", "url": "https://www.saucedemo.com/"})
# ** Можно Использовать в последовательном

@pytest_asyncio.fixture(scope="function")
async def browser_docker_session(request):
    marker = request.node.get_closest_marker("config")
    config = marker.args[0] if marker else {"browser": "chromium", "url": "https://www.saucedemo.com/"}

    browser_name = config["browser"]

    playwright = await async_playwright().start()
    print(f'\n--Запуск {browser_name} (async)--')
    browser = await playwright.chromium.connect('ws://127.0.0.1:3000/')

    try:
        yield browser
    finally:
        print('--Закрытие браузера (async)--')
        await browser.close()
        await playwright.stop()


"""Фикстуры под каждый браузер"""
@pytest_asyncio.fixture(scope="function")
# @pytest.mark.config({"browser": "chromium"})
async def browser_docker_chromium():
    """Только Chromium"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.connect('ws://127.0.0.1:3000/')
    try:
        yield browser
    finally:
        await browser.close()
        await playwright.stop()

@pytest_asyncio.fixture(scope="function")
# @pytest.mark.config({"browser": "firefox"})
async def browser_docker_firefox():
    """Только Firefox"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.connect('ws://127.0.0.1:3000/')
    try:
        yield browser
    finally:
        await browser.close()
        await playwright.stop()



"""Универсальная фикстура"""
@pytest_asyncio.fixture(scope="function")
async def universal_docker_browsers(request):
    """Возвращает все браузеры"""
    playwright = await async_playwright().start()

    chromium = await playwright.chromium.connect('ws://127.0.0.1:3000/')
    firefox = await playwright.firefox.connect('ws://127.0.0.1:3000/')

    try:
        yield {
            "chromium": chromium,
            "firefox": firefox
        }
    finally:
        await chromium.close()
        await firefox.close()
        await playwright.stop()
