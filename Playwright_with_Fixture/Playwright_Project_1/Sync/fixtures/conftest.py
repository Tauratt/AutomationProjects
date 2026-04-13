import pytest

from playwright.sync_api import sync_playwright

# C указанием браузера - в тесте по типу # @pytest.mark.config({"browser": "chromium", "url": "https://www.saucedemo.com/"})
# ** Можно Использовать в последовательном

@pytest.fixture(scope="function")
def browser_session(request):
    marker = request.node.get_closest_marker("config")
    config = marker.args[0] if marker else {"browser": "chromium", "url": "https://www.saucedemo.com/"}

    browser_name = config["browser"]

    playwright = sync_playwright().start()
    print(f'\n--Запуск {browser_name} (sync)--')
    browser = getattr(playwright, browser_name).launch(headless=False, args=["--start-maximized"])

    try:
        yield browser
    finally:
        print('--Закрытие браузера (sync)--')
        browser.close()
        playwright.stop()


"""Фикстуры под каждый браузер"""
@pytest.fixture(scope="function")
# @pytest.mark.config({"browser": "chromium"})
def browser_session_chromium():
    """Только Chromium"""
    playwright =  sync_playwright().start()
    browser =  playwright.chromium.launch(headless=False, args=["--start-maximized"])
    try:
        yield browser
    finally:
         browser.close()
         playwright.stop()

@pytest.fixture(scope="function")
# @pytest.mark.config({"browser": "firefox"})
def browser_session_firefox():
    """Только Firefox"""
    playwright =  sync_playwright().start()
    browser =  playwright.firefox.launch(headless=False, args=["--start-maximized"])
    try:
        yield browser
    finally:
         browser.close()
         playwright.stop()



"""Универсальная фикстура"""
@pytest.fixture(scope="function")
def universal_browsers_sessions(request):
    """Возвращает все браузеры"""
    playwright =  sync_playwright().start()

    chromium =  playwright.chromium.launch(headless=False, args=["--start-maximized"])
    firefox =  playwright.firefox.launch(headless=False, args=["--start-maximized"])

    try:
        yield {
            "chromium": chromium,
            "firefox": firefox
        }
    finally:
         chromium.close()
         firefox.close()
         playwright.stop()



# Использование
# def test_parallel(browsers):
#     def chrome_task():
#         # используем browsers["chromium"]
#         pass
#
#     def firefox_task():
#         # используем browsers["firefox"]
#         pass
#
#      syncio.gather(chrome_task(), firefox_task())