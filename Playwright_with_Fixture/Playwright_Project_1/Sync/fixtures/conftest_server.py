import pytest

from playwright.sync_api import sync_playwright

"""Фикстуры для запуска в Docker"""

# C указанием браузера - в тесте по типу # @pytest.mark.config({"browser": "chromium", "url": "https://www.saucedemo.com/"})
# ** Можно Использовать в последовательном

@pytest.fixture(scope="function")
def browser_docker_session(request):
    marker = request.node.get_closest_marker("config")
    config = marker.args[0] if marker else {"browser": "chromium", "url": "https://www.saucedemo.com/"}

    browser_name = config["browser"]

    playwright =  sync_playwright().start()
    print(f'\n--Запуск {browser_name} ()--')
    browser =  playwright.chromium.connect('ws://127.0.0.1:3000/')

    try:
        yield browser
    finally:
        print('--Закрытие браузера ()--')
        browser.close()
        playwright.stop()


"""Фикстуры под каждый браузер"""
@pytest.fixture(scope="function")
# @pytest.mark.config({"browser": "chromium"})
def browser_docker_chromium():
    """Только Chromium"""
    playwright =  sync_playwright().start()
    browser =  playwright.chromium.connect('ws://127.0.0.1:3000/')
    try:
        yield browser
    finally:
        browser.close()
        playwright.stop()

@pytest.fixture(scope="function")
# @pytest.mark.config({"browser": "firefox"})
def browser_docker_firefox():
    """Только Firefox"""
    playwright =  sync_playwright().start()
    browser =  playwright.chromium.connect('ws://127.0.0.1:3000/')
    try:
        yield browser
    finally:
         browser.close()
         playwright.stop()



"""Универсальная фикстура"""
@pytest.fixture(scope="function")
def universal_docker_browsers(request):
    """Возвращает все браузеры"""
    playwright =  sync_playwright().start()

    chromium =  playwright.chromium.connect('ws://127.0.0.1:3000/')
    firefox =  playwright.firefox.connect('ws://127.0.0.1:3000/')

    try:
        yield {
            "chromium": chromium,
            "firefox": firefox
        }
    finally:
         chromium.close()
         firefox.close()
         playwright.stop()
