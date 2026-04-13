import asyncio
import pytest
from playwright.async_api import async_playwright

from Playwright_Automation_Project_1.Async.pages.Cart_page import Cart
from Playwright_Automation_Project_1.Async.pages.Final_page import Final
from Playwright_Automation_Project_1.Async.config import expect, LOGIN, locators_add_to_cart
from Playwright_Automation_Project_1.Async.pages.Catalog_page import Product_Catalog_Page
from Playwright_Automation_Project_1.Async.pages.Login_page import Auth_page
import allure

from Playwright_Automation_Project_1.Async.utilities.utils import log_message

pytestmark = pytest.mark.asyncio

async def run_browser_session(p, browser_type, name: str):
    print()
    log_message(f'--Запуск браузера - {name}--')
    browser = await browser_type.connect("ws://127.0.0.1:3000/")
    context = await browser.new_context()
    page = await context.new_page()

    try:
        await page.goto("https://www.saucedemo.com/")
        await run_test_suite(page, name)
    finally:
        log_message(f'\n--Закрытие браузера - {name}--')
        await context.close()
        await browser.close()


async def run_test_suite(page, name: str):
    """
    Единая точка входа: тут собираешь ВСЕ потенциальные тесты/шаги,
    которые должны выполниться в рамках ОДНОЙ сессии браузера.
    """
    auth_page = Auth_page(page, expect)
    product_catalog_page = Product_Catalog_Page(page, expect)
    cart = Cart(page, expect,
                catalog_products=product_catalog_page.products_dict)
    final = Final(page, expect,
                products_dict=cart.products_dict)

    # 1) Авторизация
    with allure.step(f"[{name}] Авторизация пользователем {LOGIN}"):
        await auth_page.full_authorization(name)

    # 2) Работа с каталогом
    with allure.step(f"[{name}] Выбор товаров {locators_add_to_cart} и переход в корзину"):
        await product_catalog_page.select_methods()

    # 3) Работа с Корзиной
    with allure.step(f"Проверка товаров в корзине"):
        await cart.select_methods()

    # 4) Финальная страница
    with allure.step(f"Проверка товаров на Финальной странице"):
        await final.select_methods()


async def test_full_path():
    async with async_playwright() as p:
        print("🚀 Запуск последовательный\n")

        # Chromium
        await run_browser_session(p, p.chromium, "Chromium")

        # Firefox
        await run_browser_session(p, p.firefox, "Firefox")

        print("\n🎉 Все тесты завершены!")
