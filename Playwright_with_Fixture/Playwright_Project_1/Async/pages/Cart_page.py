import random

import allure

from Playwright_with_Fixture.Playwright_Project_1.Async.utilities.utils import (
    log_message, error, success, step
)
from Playwright_with_Fixture.Playwright_Project_1.Async.base.base_class import Settings

from Playwright_with_Fixture.Playwright_Project_1.Async.config import (
    INVENTORY_ITEM_NAME_CART,
    INVENTORY_ITEM_PRICE_CART,
    checkout_button_locator,
    fake,
    title_user_info,
    word_user_info_page,
    postal_code_field,
    first_name_field,
    last_name_field, button_continue, INVENTORY_ITEM_CART
)

from Playwright_with_Fixture.Playwright_Project_1.Async.helper_func.error_class import (
    LocatorNotFoundError
)
from Playwright_with_Fixture.Playwright_Project_1.Async.utilities.utils import (
    error,
    log_message,
    step
)
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class Cart(Settings):
    def __init__(self, page, expect, catalog_products):
        super().__init__(page, expect)
        self.products_dict = catalog_products
        # Инициализация Cart если её нет
        if 'Cart' not in self.products_dict:
            self.products_dict['Cart'] = {}

    @allure.step("Получение Name и Price в Корзине")
    async def get_names_prices(self):
        cards = self.page.locator(INVENTORY_ITEM_CART)
        await self.check_expect_exists(cards, timeout=5000, name="Cart items")

        count = await cards.count()

        for i in range(count):
            card = cards.nth(i)
            name = (await card.locator(INVENTORY_ITEM_NAME_CART).inner_text()).strip()
            price = (await card.locator(INVENTORY_ITEM_PRICE_CART).inner_text()).strip()

            self.products_dict['Cart'].setdefault(name, []).append(price)

    @allure.step("Проверка добавленных товаров в Корзине")
    async def check_products_in_the_cart(self):
        log_message('Check Products in the Cart:')
        try:
            await self.get_names_prices()

            catalog = self.products_dict.get('Catalog', {})
            cart = self.products_dict.get('Cart', {})

            for name, catalog_prices in catalog.items():
                if name in cart:
                    success(f'\tНазвание({name}) с Каталога и Корзины совпадают')
                else:
                    error(f'\tНазвание({name}) с Каталога и Корзины НЕ совпадают')

                cart_prices = cart.get(name, [])

                if cart_prices == catalog_prices:
                    success(f'\t{name} - Цена({cart_prices}) с Каталога и Корзины совпадают\n')
                else:
                    error(
                        f'\t{name} - Цена({cart_prices}) с Каталога и Корзины НЕ совпадают: '
                        f'catalog={catalog_prices}, cart={cart_prices}\n'
                    )

        except LocatorNotFoundError as e:
            error(str(e))
            raise
        except AssertionError as ae:
            error(str(ae))
        except Exception as e:
            error(str(e))

    @allure.step("Нажатие кнопки - Checkout")
    async def checkout_button(self):
        log_message('Checkout Button:')
        try:
            button = self.page.locator(checkout_button_locator)
            await self.check_expect_count(button, 1, timeout=5000, name="Cart Checkout Button")
            await button.click()
            step('Click Checkout Button:')

            title = self.page.locator(title_user_info)
            await self.expect(title).to_have_text(word_user_info_page)
            success('\tCheck Click Checkout Button - GOOD')
            return True

        except LocatorNotFoundError as e:
            error(str(e))
            return False
        except AssertionError as ae:
            error('\tCheck Click Checkout Button - BAD')
            return False
        except Exception as e:
            error(str(e))
            return False

    @allure.step("Заполнение информации пользователя")
    async def input_user_info(self):
        log_message('Input User Info:')
        try:
            name = fake.first_name()
            last_name = fake.last_name()
            postal_code = fake.postcode()

            name_field = self.page.locator(first_name_field)
            last_field = self.page.locator(last_name_field)
            code_field = self.page.locator(postal_code_field)

            await self.check_expect_count(name_field, 1, timeout=5000, name="First Name Field")
            await self.check_expect_count(last_field, 1, timeout=5000, name="Last Name Field")
            await self.check_expect_count(code_field, 1, timeout=5000, name="Postal Code Field")

            await name_field.fill(name)
            await last_field.fill(last_name)
            await code_field.fill(postal_code)

            # Проверка введённых значений через assert (если не совпало — AssertionError)
            v1 = await name_field.input_value()
            v2 = await last_field.input_value()
            v3 = await code_field.input_value()

            assert v1 == name, f'First name mismatch: expected="{name}", got="{v1}"'
            assert v2 == last_name, f'Last name mismatch: expected="{last_name}", got="{v2}"'
            assert v3 == postal_code, f'Postal code mismatch: expected="{postal_code}", got="{v3}"'

            success("\tUser info filled")
            return True

        except LocatorNotFoundError as e:
            error(str(e))
            raise
        except AssertionError as ae:
            error(str(ae))
            return False
        except PlaywrightTimeoutError as e:
            error(f'Input user info PlaywrightTimeoutError: {e}')
            return False
        except Exception as e:
            error(f'Input user info error: {e}')
            return False


    @allure.step("Нажатие кнопки - Continue")
    async def click_button_continue(self):
        log_message('Button Continue:')
        try:
            step('Button Continue:')
            button = self.page.locator(button_continue)
            await self.check_expect_count(button, 1, timeout=5000, name="Button Continue")
            await button.click()
            success('\tClick Continue Button')
            return True

        except LocatorNotFoundError as e:
            error(str(e))
            raise
        except AssertionError as ae:
            error(str(ae))
            return False
        except Exception as e:
            error(f'Button Continue: {e}')
            return False

    @allure.step("Основной рабочий поток корзины")
    async def select_methods(self):
        log_message("=" * 50)
        log_message(f'{'='*16} Modul Name:{self.__class__.__name__} {'='*16}')
        await self.get_current_url()
        await self.check_products_in_the_cart()
        checkout_result = await self.checkout_button()
        if checkout_result:
            user_info_result =  await self.input_user_info()
            if user_info_result:
                await self.click_button_continue()
        else:
            error("Checkout failed, skipping user info input")