import os

from playwright.sync_api import expect
from pathlib import Path
from faker import Faker

fake = Faker("ru_RU")

expect.set_options(timeout=5_000)  # все expect(...) теперь ждут до 10 секунд
# Как изменить время ожидания
# Для одного конкретного ожидания:

# expect(logo).to_have_text("Swag Labs", timeout=10_000)  # 10 секунд

# Глобально (через конфиг / set_options в Python):
# Если используешь свой обёрточный конфиг, обычно делают что‑то вроде:

# from playwright.sync_api import expect
# expect.set_options(timeout=10_000)  # все expect(...) теперь ждут до 10 секунд

"""SCREENSHOT_DIR"""

current_dir = os.getcwd()
path_sc = os.path.abspath(os.path.join(current_dir, "screenshots"))
os.makedirs(path_sc, exist_ok=True)
SCREENSHOT_DIR = path_sc



login_field = "#user-name"
password_field = "#password"
login_button = "#login-button"

LOGIN = "standard_user"
PASSWORD = "secret_sauce"

"""Titles с каждой страницы"""
Logo_login_page = '.login_logo'
Logo_catalog = ".app_logo" # Страница Главная(Каталог)
title_user_info = '[data-test="title"]' # Страница заполнение информации пользователя
title_final_page = '[data-test="complete-header"]'

"""Тексты проверки с каждой страницы"""
word_login_page = 'Swag Labs'
word_catalog_page = 'Swag Labs'
word_user_info_page = 'Checkout: Your Information'
word_final_page = 'Thank you for your order!'

"""Меню - Каталог"""
menu_button = '#react-burger-menu-btn'
menu_button_logout = '[data-test="logout-sidebar-link"]'


"""Константы каждой карточки товара(внутри него - название, цена, кнопка добавить итд) - Каталог"""
INVENTORY_ITEM_CARD = ".inventory_item"  # Каждая Карточка товара в списке (контейнер name/price/button).
INVENTORY_ITEM_NAME = '[data-test="inventory-item-name"]'  # Название товара внутри карточки.
INVENTORY_ITEM_PRICE = '[data-test="inventory-item-price"]'  # Цена товара внутри карточки.


"""Выбранные продукты для добавления в корзину - Кнопка add-to-cart - Каталог"""
product1 = '[data-test="add-to-cart-sauce-labs-backpack"]'
product2 = '[data-test="add-to-cart-sauce-labs-bike-light"]'
product3 = '[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]'
product4 = '[data-test="add-to-cart-sauce-labs-fleece-jacket"]'
product5 = '[data-test="add-to-cart-sauce-labs-onesie"]'
product6 = '[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]'

# Список для удобства
locators_add_to_cart = [
    product1, product2,
    product3, product4,
    product5, product6
]


"""Корзина"""
cart_button = '#shopping_cart_container' # locator()
checkout_button_locator = '[data-test="checkout"]'

"""Константы каждой карточки товара(внутри него - название, цена, кнопка добавить итд) - Корзина"""
INVENTORY_ITEM_CART = ".cart_item"  # Карточка товара в списке (контейнер name/price/button).
INVENTORY_ITEM_NAME_CART = '[data-test="inventory-item-name"]'  # Название товара внутри карточки.
INVENTORY_ITEM_PRICE_CART = '[data-test="inventory-item-price"]'  # Цена товара внутри карточки.

"""Страница ввода пользовательской информации"""
first_name_field = '[data-test="firstName"]'
last_name_field = '[data-test="lastName"]'
postal_code_field = '[data-test="postalCode"]'
button_continue = '[data-test="continue"]'

"""Константы каждой карточки товара(внутри него - название, цена, кнопка добавить итд) - Финальная страница"""
INVENTORY_ITEM_CARDS_FINAL = '.cart_item'
INVENTORY_ITEM_NAME_FINAL = '[data-test="inventory-item-name"]'
INVENTORY_ITEM_PRICE_FINAL = '[data-test="inventory-item-price"]'
total_sum_locator = '[data-test="subtotal-label"]'
button_finish = '[data-test="finish"]'
back_home_button = '[data-test="back-to-products"]'







# ==========================================Не используется в коде============================
"""Имя продукта - Каталог"""
name_product1 = '[data-test="item-4-title-link"]'
name_product2 = '[data-test="item-0-title-link"]'
name_product3 = '[data-test="item-1-title-link"]'
name_product4 = '[data-test="item-5-title-link"]'
name_product5 = '[data-test="item-2-title-link"]'
name_product6 = '[data-test="item-3-title-link"]'

"""Цена продукта - Каталог"""
price_product1 = '#add-to-cart-sauce-labs-backpack'
price_product2 = '#add-to-cart-sauce-labs-bike-light'
price_product3 = '#add-to-cart-sauce-labs-bolt-t-shirt'
price_product4 = '#add-to-cart-sauce-labs-fleece-jacket'
price_product5 = '#add-to-cart-sauce-labs-onesie'
price_product6 = '[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]'

"""Кнопка Remove - Корзина"""
cart_product1 = '[data-test="remove-sauce-labs-bike-light"]'
cart_product2 = '[data-test="remove-sauce-labs-backpack"]'
cart_product3 = '[data-test="remove-sauce-labs-bolt-t-shirt"]'
cart_product4 = '[data-test="remove-sauce-labs-fleece-jacket"]'
cart_product5 = '[data-test="remove-test.allthethings()-t-shirt-(red)"]'
cart_product6 = '[data-test="remove-sauce-labs-onesie"]'

# ========================================================================
# ===============================Не используется в коде===================
"""Проверка появления Remove на кнопке Add to cart после нажатия - Каталог"""
r_product1 = '#remove-sauce-labs-backpack'
r_product2 = '#remove-sauce-labs-bike-light'
r_product3 = '#remove-sauce-labs-bolt-t-shirt'
r_product4 = '#remove-sauce-labs-fleece-jacket'
r_product5 = '#remove-sauce-labs-onesie'
r_product6 = '[data-test="remove-test.allthethings()-t-shirt-(red)"]'

remove_locator_product_list = [
    r_product1, r_product2,
    r_product3, r_product4,
    r_product5, r_product6
]
# ========================================================================