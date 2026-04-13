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
from Playwright_with_Fixture.Playwright_Project_1.Sync.fixtures.conftest import (browser_session_chromium,
    browser_session_firefox, universal_browsers_sessions, browser_session)


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



"""Фикстура C указанием браузера - browser_session"""
@pytest.mark.config({"browser": "chromium", "url": "https://www.saucedemo.com/"})
def test_specified_browsers1(browser_session):
    context1 =  browser_session.new_context(no_viewport=True)
    page1 =  context1.new_page()
    page1.goto("https://www.saucedemo.com/")

    run_test_suite(page1, name_browser='firefox')
    print(f'Firefox: { page1.title()}')

    page1.close()
    context1.close()


"""Фикстура C указанием браузера - browser_session"""
@pytest.mark.config({"browser": "firefox", "url": "https://www.saucedemo.com/"})
def test_specified_browsers2(browser_session):
    context1 =  browser_session.new_context(no_viewport=True)
    page1 =  context1.new_page()
    page1.goto("https://www.saucedemo.com/")

    run_test_suite(page1, name_browser='firefox')
    print(f'Firefox: { page1.title()}')

    page1.close()
    context1.close()



"""Фикстура - browser_session_firefox"""
def test_firefox(browser_session_firefox):
    context1 =  browser_session_firefox.new_context(no_viewport=True)
    page1 =  context1.new_page()
    page1.goto("https://www.saucedemo.com/")

    run_test_suite(page1, name_browser='firefox')
    print(f'Firefox: { page1.title()}')

    page1.close()
    context1.close()
#


"""Фикстура - browser_session_chromium"""
def test_chrome(browser_session_chromium):
    context1 =  browser_session_chromium.new_context(no_viewport=True)
    page1 =  context1.new_page()
    page1.goto("https://www.saucedemo.com/")

    run_test_suite(page1, name_browser='chrome')
    print(f'Chrome: { page1.title()}')

    page1.close()
    context1.close()


"""Фикстура возвращающая все браузеры(chrom, firefox) - universal_browsers_sessions"""
def test_browsers(universal_browsers_sessions):
    context1 =  universal_browsers_sessions["firefox"].new_context(no_viewport=True)
    page1 =  context1.new_page()
    page1.goto("https://www.saucedemo.com/")

    run_test_suite(page1, name_browser='chrome')
    print(f'Chrome: { page1.title()}')

    page1.close()
    context1.close()