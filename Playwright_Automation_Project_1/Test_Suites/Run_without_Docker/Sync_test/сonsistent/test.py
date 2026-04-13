import allure
from Playwright_Automation_Project_1.Sync.config import (
    expect, LOGIN, locators_add_to_cart
)
from Playwright_Automation_Project_1.Sync.pages.Cart_page import Cart
from Playwright_Automation_Project_1.Sync.pages.Catalog_page import Product_Catalog_Page
from Playwright_Automation_Project_1.Sync.pages.Final_page import Final
from Playwright_Automation_Project_1.Sync.pages.Login_page import Auth_page
from Playwright_Automation_Project_1.Sync.utilities.utils import log_message
from playwright.sync_api import sync_playwright




def run_test_suite(page, name: str):
    """
    Единая точка входа: все тесты/шаги в рамках одной сессии.
    """
    auth_page = Auth_page(page, expect)  # ← Передаем name!
    product_catalog_page = Product_Catalog_Page(page, expect)
    cart = Cart(page, expect, catalog_products=product_catalog_page.products_dict)
    final = Final(page, expect, products_dict=cart.products_dict)


    # 1) Авторизация
    with allure.step(f"[{name}] Авторизация пользователем {LOGIN}"):
        auth_page.full_authorization(name)

    # 2) Каталог
    with allure.step(f"[{name}] Выбор товаров {locators_add_to_cart}"):
        product_catalog_page.select_methods()

    # 3) Корзина
    with allure.step(f"Проверка товаров в корзине"):
        cart.select_methods()

    # 4) Финал
    with allure.step(f"Проверка на финальной странице"):
        final.select_methods()



def run_browser_session(p, browser_type, name: str):
    print()
    log_message(f'--Запуск браузера - {name}--')

    browser = browser_type.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    try:
        page.goto("https://www.saucedemo.com/")
        run_test_suite(page, name)
    finally:
        log_message(f'\n--Закрытие браузера - {name}--')
        context.close()
        browser.close()


def test_full_path():  # ← def!
    """Синхронный тест — ПОСЛЕДОВАТЕЛЬНО"""
    with sync_playwright() as p:
        print("🚀 Запуск синхронный\n")

        # Chromium
        run_browser_session(p, p.chromium, "Chromium")

        # Firefox (ПОСЛЕ Chromium)
        run_browser_session(p, p.firefox, "Firefox")

        print("\n🎉 Все тесты завершены!")


# Запуск
if __name__ == "__main__":
    test_full_path()