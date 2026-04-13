import asyncio

import pytest
import pytest_asyncio
import allure
from playwright.async_api import async_playwright
from Playwright_with_Fixture.Playwright_Project_1.Async.config import (
    expect, LOGIN, locators_add_to_cart
)
from Playwright_with_Fixture.Playwright_Project_1.Async.pages.Cart_page import Cart
from Playwright_with_Fixture.Playwright_Project_1.Async.pages.Catalog_page import Product_Catalog_Page
from Playwright_with_Fixture.Playwright_Project_1.Async.pages.Final_page import Final
from Playwright_with_Fixture.Playwright_Project_1.Async.pages.Login_page import Auth_page
from Playwright_with_Fixture.Playwright_Project_1.Async.utilities.utils import log_message
from Playwright_with_Fixture.Playwright_Project_1.Async.fixtures.conftest import (browser_session_chromium,
    browser_session_firefox, universal_browsers_sessions, browser_session)
import pytest_asyncio

async def run_test_suite(page, name_browser: str):
    """
    Единая точка входа: все тесты/шаги в рамках одной сессии (ASYNC).
    """
    auth_page = Auth_page(page, expect)
    product_catalog_page = Product_Catalog_Page(page, expect)
    cart = Cart(page, expect, catalog_products=product_catalog_page.products_dict)
    final = Final(page, expect, products_dict=cart.products_dict)

    # 1) Авторизация
    with allure.step(f"[{name_browser}] Авторизация пользователем {LOGIN}"):
        await auth_page.full_authorization(name_browser)

    # 2) Каталог
    with allure.step(f"[{name_browser}] Выбор товаров {locators_add_to_cart}"):
        await product_catalog_page.select_methods()

    # 3) Корзина
    with allure.step(f"Проверка товаров в корзине"):
        await cart.select_methods()

    # 4) Финал
    with allure.step(f"Проверка на финальной странице"):
        await final.select_methods()


"""Фикстура C указанием браузера - browser_session"""
@pytest.mark.config({"browser": "chromium", "url": "https://www.saucedemo.com/"})
async def test_specified_browsers1(browser_session):
    context1 = await browser_session.new_context(no_viewport=True)
    page1 = await context1.new_page()
    await page1.goto("https://www.saucedemo.com/")

    await run_test_suite(page1, name_browser='firefox')
    print(f'Firefox: {await page1.title()}')

    await page1.close()
    await context1.close()


"""Фикстура C указанием браузера - browser_session"""
@pytest.mark.config({"browser": "firefox", "url": "https://www.saucedemo.com/"})
async def test_specified_browsers2(browser_session):
    context1 = await browser_session.new_context(no_viewport=True)
    page1 = await context1.new_page()
    await page1.goto("https://www.saucedemo.com/")

    await run_test_suite(page1, name_browser='firefox')
    print(f'Firefox: {await page1.title()}')

    await page1.close()
    await context1.close()



"""Фикстура - browser_session_firefox"""
async def test_firefox(browser_session_firefox):
    context1 = await browser_session_firefox.new_context(no_viewport=True)
    page1 = await context1.new_page()
    await page1.goto("https://www.saucedemo.com/")

    await run_test_suite(page1, name_browser='firefox')
    print(f'Firefox: {await page1.title()}')

    await page1.close()
    await context1.close()
#


"""Фикстура - browser_session_chromium"""
async def test_chrome(browser_session_chromium):
    context1 = await browser_session_chromium.new_context(no_viewport=True)
    page1 = await context1.new_page()
    await page1.goto("https://www.saucedemo.com/")

    await run_test_suite(page1, name_browser='chrome')
    print(f'Chrome: {await page1.title()}')

    await page1.close()
    await context1.close()


"""Фикстура возвращающая все браузеры(chrom, firefox) - universal_browsers_sessions"""
async def test_browsers(universal_browsers_sessions):
    context1 = await universal_browsers_sessions["firefox"].new_context(no_viewport=True)
    page1 = await context1.new_page()
    await page1.goto("https://www.saucedemo.com/")

    await run_test_suite(page1, name_browser='chrome')
    print(f'Chrome: {await page1.title()}')

    await page1.close()
    await context1.close()



"""Фикстура(или набор фикстур, они универсальны под asyncio.gather). Под Параллельный запуск(asyncio.gather)"""
async def test_parallel_browsers(browser_session):

    # """Chrome + Firefox ПАРАЛЛЕЛЬНО!"""
    # async def chrome_suite():
    #     context = await browser_session_chromium.new_context(no_viewport=True)
    #     page = await context.new_page()
    #     await page.goto("https://www.saucedemo.com/")
    #     await run_test_suite(page, "Chrome")
    #     print(f'Chrome: {await page.title()}')
    #     await page.close()
    #     await context.close()
    #
    # async def firefox_suite():
    #     context = await browser_session_firefox.new_context(no_viewport=True)
    #     page = await context.new_page()
    #     await page.goto("https://www.saucedemo.com/")
    #     await run_test_suite(page, "Firefox")
    #     print(f'Firefox: {await page.title()}')
    #     await page.close()
    #     await context.close()

    await asyncio.gather(test_specified_browsers1(browser_session), test_specified_browsers2(browser_session))