import allure

from Playwright_with_Fixture.Playwright_Project_1.Async.utilities.utils import (
    log_message, error, success, step
)
from Playwright_with_Fixture.Playwright_Project_1.Async.base.base_class import Settings

from Playwright_with_Fixture.Playwright_Project_1.Async.config import (
    INVENTORY_ITEM_NAME_FINAL,
    INVENTORY_ITEM_PRICE_FINAL,
    INVENTORY_ITEM_CARDS_FINAL,
    button_finish,
    total_sum_locator,
    word_final_page,
    title_final_page,
    back_home_button,
    Logo_catalog,
    word_catalog_page,
    menu_button,
    menu_button_logout,
    Logo_login_page,
    word_login_page
)

from Playwright_with_Fixture.Playwright_Project_1.Async.helper_func.error_class import (
    LocatorNotFoundError
)


class Final(Settings):
    def __init__(self, page, expect, products_dict):
        super().__init__(page, expect)
        self.products_dict = products_dict


    async def _get_names_prices(self):
        cards = self.page.locator(INVENTORY_ITEM_CARDS_FINAL)
        await self.check_expect_exists(cards, timeout=5000, name="Final items")

        count = await cards.count()

        for i in range(count):
            card = cards.nth(i)
            name = (await card.locator(INVENTORY_ITEM_NAME_FINAL).inner_text()).strip()
            price = (await card.locator(INVENTORY_ITEM_PRICE_FINAL).inner_text()).strip()

            self.products_dict['FinalPage'].setdefault(name, []).append(price)

    @allure.step("Проверка товаров в Корзине и на Финальной странице")
    async def check_products_final_page(self):
        log_message('Check Products in the Final Page:')
        try:
            await self._get_names_prices()

            cart = self.products_dict.get('Cart', {})
            final_page = self.products_dict.get('FinalPage', {})

            for name, final_page_prices in final_page.items():
                if name in cart:
                    success(f'\tНазвание({name}) с Корзины и на Финальной странице совпадают')
                else:
                    error(f'\tНазвание({name}) с Корзины и на Финальной странице НЕ совпадают')

                cart_prices = cart.get(name, [])

                if cart_prices == final_page_prices:
                    success(f'\t{name} - Цена({cart_prices}) с Корзины и на Финальной странице совпадают\n')
                else:
                    error(
                        f'\t{name} - Цена({cart_prices}) с Корзины и на Финальной странице НЕ совпадают: '
                        f'catalog={final_page_prices}, cart={cart_prices}\n'
                    )

        except LocatorNotFoundError as e:
            error(str(e))
            raise
        except AssertionError as ae:
            error(str(ae))
        except Exception as e:
            error(str(e))

    async def _get_total_sum(self):
        locator = self.page.locator(total_sum_locator)
        await self.check_expect_count(locator, 1, timeout=5000, name="Total Sum Locator")

        total_sum_text = (await locator.inner_text()).strip()  # например: "Item total: $129.94"
        replace_total_sum = total_sum_text.replace('Item total:', '').replace('$', '').strip()

        return float(replace_total_sum)

    @allure.step("Проверка итоговой суммы")
    async def check_total_sum(self):
        log_message('Total Sum:')
        try:
            total_sum_final = 0
            final_page = self.products_dict.get('FinalPage', {})

            for k, v in final_page.items():
                for v2 in v:
                    replace_price = float(v2.replace('$', ''))
                    total_sum_final += replace_price

            total_sum_cart = await self._get_total_sum()
            assert total_sum_final == total_sum_cart, \
                f'Total sum mismatch: calculated={total_sum_final}, page={total_sum_cart}'

            success(f'\tCheck Total Summ: {total_sum_final}$ - GOOD')

        except LocatorNotFoundError as e:
            error(str(e))
            raise
        except ValueError as ve:
            error(f'Value conversion error: {ve}')
            raise
        except AssertionError as ae:
            error(str(ae))
        except Exception as e:
            error(str(e))

    @allure.step("Нажатие кнопки - Finish")
    async def finish_button(self):
        log_message('Finish Button:')
        try:
            button = self.page.locator(button_finish)
            await self.check_expect_count(button, 1, timeout=5000, name="Finish Button")
            await button.click()
            step('Click Finish Button:')

            title = self.page.locator(title_final_page)
            await self.expect(title).to_have_text(word_final_page)
            success('\tCheck Click Finish Button - GOOD')
            return True

        except LocatorNotFoundError as e:
            error(str(e))
            return False
        except AssertionError as ae:
            error('\tCheck Click Finish Button - BAD')
            return False
        except Exception as e:
            error(str(e))
            return False

    @allure.step("Нажатие кнопки - Back Home")
    async def click_button_back_home(self):
        log_message('Button Back Home:')
        try:
            button = self.page.locator(back_home_button)
            await self.check_expect_count(button, 1, timeout=5000, name="Back Home Button")
            await button.click()
            step('Click Back Home Button:')

            title = self.page.locator(Logo_catalog)
            await self.expect(title).to_have_text(word_catalog_page)
            success('\tCheck Click Back Home Button - GOOD')
            return True

        except LocatorNotFoundError as e:
            error(str(e))
            return False
        except AssertionError as ae:
            error('\tCheck Click Back Home Button - BAD')
            return False
        except Exception as e:
            error(str(e))
            return False

    @allure.step("Разлогинивание")
    async def logout(self):
        log_message('Logout:')
        try:
            button = self.page.locator(menu_button)
            await self.check_expect_count(button, 1, timeout=5000, name="Menu Button")
            await button.click()
            step('\tClick Menu Button')

            logout_button = self.page.locator(menu_button_logout)
            await self.check_expect_count(logout_button, 1, timeout=5000, name="Logout Button")
            await logout_button.click()
            step('\tClick Logout Button')

            # ✅ ИСПРАВЛЕНО: expect должен работать с locator
            title = self.page.locator(Logo_login_page)
            await self.expect(title).to_have_text(word_login_page)
            success('\t\tCheck Logout - GOOD')
            return True

        except LocatorNotFoundError as e:
            error(str(e))
            return False
        except AssertionError as ae:
            error('\tCheck Logout - BAD')
            return False
        except Exception as e:
            error(str(e))
            return False

    @allure.step("Основной рабочий поток финальной страницы")
    async def select_methods(self):
        log_message("=" * 50)
        log_message(f'{'=' * 16} Modul Name:{self.__class__.__name__} {'=' * 16}')
        await self.get_current_url()
        await self.check_products_final_page()
        await self.check_total_sum()
        if await self.finish_button():
            if await self.click_button_back_home():
                await self.logout()
