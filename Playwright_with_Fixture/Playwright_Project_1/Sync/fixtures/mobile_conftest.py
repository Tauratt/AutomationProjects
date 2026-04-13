import pytest
from playwright.sync_api import sync_playwright


"""Фикстуры под каждый браузер"""
@pytest.fixture(scope="function")
# @pytest.mark.config({"browser": "chromium"})
def browser_mobile_chromium():
    """Только Chromium"""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    try:
        yield browser, playwright
    finally:
         browser.close()
         playwright.stop()


@pytest.fixture(scope="function")
def browser_mobile_webkit():
    """Только webkit"""
    playwright =  sync_playwright().start()
    browser =  playwright.webkit.launch(headless=False)
    try:
        yield browser, playwright
    finally:
        browser.close()
        playwright.stop()


@pytest.fixture(scope="function")
# @pytest.mark.config({"browser": "firefox"})
def browser_mobile_firefox():
    """Только Firefox"""
    playwright =  sync_playwright().start()
    browser =  playwright.firefox.launch(headless=False)
    try:
        yield browser, playwright
    finally:
         browser.close()
         playwright.stop()



# C указанием браузера - в тесте по типу # @pytest.mark.config({"browser": "chromium", "url": "https://www.saucedemo.com/"})
# ** Можно Использовать в последовательном

@pytest.fixture(scope="function")
def browser_mobile_session(request):
    marker = request.node.get_closest_marker("config")
    config = marker.args[0] if marker else {"browser": "chromium", "url": "https://www.saucedemo.com/"}

    browser_name = config["browser"]

    playwright = sync_playwright().start()
    print(f'\n--Запуск {browser_name} (sync)--')
    browser =  getattr(playwright, browser_name).launch(headless=False)

    try:
        yield browser, playwright
    finally:
        print('--Закрытие браузера (sync)--')
        browser.close()
        playwright.stop()



"""Универсальная фикстура"""
@pytest.fixture(scope="function")
def universal_browsers_mobile_sessions():
    """Возвращает все браузеры"""
    playwright =  sync_playwright().start()

    chromium =  playwright.chromium.launch(headless=False)
    firefox =  playwright.firefox.launch(headless=False)
    webkit =  playwright.webkit.launch(headless=False)

    try:
        yield {
            "chromium": chromium,
            "firefox": firefox,
            "webkit":webkit
        }, playwright
    finally:
         chromium.close()
         firefox.close()
         playwright.stop()


