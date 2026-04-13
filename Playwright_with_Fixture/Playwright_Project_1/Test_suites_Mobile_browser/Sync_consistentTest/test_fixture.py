import pytest
from playwright.sync_api import sync_playwright
import allure
from Playwright_with_Fixture.Playwright_Project_1.Sync.config import (
    expect, LOGIN, locators_add_to_cart)
from Playwright_with_Fixture.Playwright_Project_1.Sync.pages.Cart_page import Cart
from Playwright_with_Fixture.Playwright_Project_1.Sync.pages.Catalog_page import Product_Catalog_Page
from Playwright_with_Fixture.Playwright_Project_1.Sync.pages.Final_page import Final
from Playwright_with_Fixture.Playwright_Project_1.Sync.pages.Login_page import Auth_page
from Playwright_with_Fixture.Playwright_Project_1.Sync.utilities.utils import log_message
from Playwright_with_Fixture.Playwright_Project_1.Sync.fixtures.mobile_conftest import *


def run_test_suite(page, name_browser: str):
    """
    Единая точка входа: все тесты/шаги в рамках одной сессии.
    """
    auth_page = Auth_page(page, expect)  # ← Передаем name!
    product_catalog_page = Product_Catalog_Page(page, expect)
    cart = Cart(page, expect, catalog_products=product_catalog_page.products_dict)
    final = Final(page, expect, products_dict=cart.products_dict)


    # 1) Авторизация
    with allure.step(f"[{name_browser}] Авторизация пользователем {LOGIN}"):
        auth_page.full_authorization(name_browser)

    # 2) Каталог
    with allure.step(f"[{name_browser}] Выбор товаров {locators_add_to_cart}"):
        product_catalog_page.select_methods()

    # 3) Корзина
    with allure.step(f"Проверка товаров в корзине"):
        cart.select_methods()

    # 4) Финал
    with allure.step(f"Проверка на финальной странице"):
        final.select_methods()



"""Фикстура - browser_mobile_session"""
@pytest.mark.config({"browser": "chromium", "url": "https://www.saucedemo.com/"})
def test_chrome1(browser_mobile_session):
    browser, p = browser_mobile_session
    device_config = p.devices["iPhone 14 Pro"]

    context1 =  browser.new_context(**device_config)
    page1 =  context1.new_page()
    page1.goto("https://www.saucedemo.com/")

    run_test_suite(page1, name_browser='Mobile-chrome')
    print(f'Chrome: { page1.title()}')

    page1.close()
    context1.close()


"""Фикстура - browser_mobile_chromium"""
def test_chrome2(browser_mobile_chromium):
    browser, p = browser_mobile_chromium
    device_config = p.devices["Pixel 5"]

    context1 =  browser.new_context(**device_config)
    page1 =  context1.new_page()
    page1.goto("https://www.saucedemo.com/")

    run_test_suite(page1, name_browser='Mobile-chrome')
    print(f'Chrome: { page1.title()}')

    page1.close()
    context1.close()


"""Фикстура - browser_mobile_webkit"""
def test_webkit(browser_mobile_webkit):
    browser, p = browser_mobile_webkit
    device_config = p.devices["iPhone 14 Pro"]

    context1 =  browser.new_context(**device_config)
    page1 =  context1.new_page()
    page1.goto("https://www.saucedemo.com/")

    run_test_suite(page1, name_browser='Mobile-Webkit')
    print(f'Webkit: { page1.title()}')

    page1.close()
    context1.close()



"""Фикстура - universal_browsers_mobile_sessions)"""
def test_universal_browsers(universal_browsers_mobile_sessions):
    browser, p = universal_browsers_mobile_sessions
    device_config = p.devices["iPhone 14 Pro"]

    context1 =  browser['webkit'].new_context(**device_config)
    page1 =  context1.new_page()
    page1.goto("https://www.saucedemo.com/")

    run_test_suite(page1, name_browser='Mobile-webkit')
    print(f'webkit: {page1.title()}')

    page1.close()
    context1.close()



"""Фикстура C указанием браузера - browser_mobile_session"""
def test_firefox1(browser_mobile_firefox):
    browser, p = browser_mobile_firefox

    # ✅ ФИЛЬТР для Firefox (убираем isMobile)
    device = p.devices["iPhone 14 Pro"].copy()
    if "is_mobile" in device:
        del device["is_mobile"]  # Firefox НЕ поддерживает!
    if "has_touch" in device:
        del device["has_touch"]  # Firefox НЕ поддерживает!

    context1 =  browser.new_context(**device)
    page1 =  context1.new_page()
    page1.goto("https://www.saucedemo.com/")

    run_test_suite(page1, name_browser='firefox')
    print(f'Firefox: {page1.title()}')

    page1.close()
    context1.close()



def test_firefox2(browser_mobile_firefox):
    browser, p = browser_mobile_firefox

    # ✅ ФИЛЬТР для Firefox (убираем isMobile) Firefox НЕ поддерживает мобильную эмуляцию!
    device = p.devices["Pixel 5"].copy()
    if "is_mobile" in device:
        del device["is_mobile"]  # Firefox НЕ поддерживает!
    if "has_touch" in device:
        del device["has_touch"]  # Firefox НЕ поддерживает!

    context1 =  browser.new_context(**device)
    page1 =  context1.new_page()

    try:
        page1.goto("https://www.saucedemo.com/")
        run_test_suite(page1, name_browser='Firefox Pixel 5')
        print(f'✅ Firefox Pixel 5: { page1.title()}')
    finally:
        page1.close()
        context1.close()

