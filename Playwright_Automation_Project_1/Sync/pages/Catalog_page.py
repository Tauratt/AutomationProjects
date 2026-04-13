import time
import allure
from Playwright_Automation_Project_1.Sync.base.base_class import Settings
from Playwright_Automation_Project_1.Sync.config import (
    cart_button,
    locators_add_to_cart, INVENTORY_ITEM_CARD, INVENTORY_ITEM_NAME, INVENTORY_ITEM_PRICE
)
from Playwright_Automation_Project_1.Sync.helper_func.error_class import \
    LocatorNotFoundError
from Playwright_Automation_Project_1.Sync.utilities.utils import (
    log_message, error,
    success, step
)
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class Product_Catalog_Page(Settings):
    def __init__(self, page, expect):
        super().__init__(page, expect)

        self.products_dict = {
            'Catalog': {},
            'Cart': {},
            'FinalPage':{}
        }

    @allure.step("Добавление товаров в корзину (Add to cart)")
    def click_add_to_cart(self, locators_add_to_cart):
        log_message("Adding Products to the Cart:")
        step('\tCheck Click Add to Cart:')
        for button_locator in locators_add_to_cart:
            try:
                add_button = self.page.locator(button_locator)
                # 1) Ждём, что кнопка реально существует в единственном экземпляре
                self.check_expect_count(add_button, 1, timeout=5000, name="Add button")

                # 2) Находим карточку по filter(has=add_button) и ждём, что карточка ровно одна
                card = self.page.locator(INVENTORY_ITEM_CARD).filter(has=add_button)
                self.check_expect_count(card, 1, timeout=5000, name="Inventory card")

                # 3) Дальше можно безопасно доставать текст и кликать
                name = (card.locator(INVENTORY_ITEM_NAME).text_content() or "").strip()
                price = (card.locator(INVENTORY_ITEM_PRICE).inner_text() or "").strip()

                add_button.scroll_into_view_if_needed()
                add_button.click()

                if self._check_click_add_to_cart(button_locator):
                    success(f"\tAdd to cart OK: {button_locator}")
                    self.products_dict['Catalog'].setdefault(name, []).append(price)
                else:
                    error(f"Add to cart failed: {button_locator}")

            except LocatorNotFoundError as e:
                error(str(e))
                continue

            except PlaywrightTimeoutError as e:
                error(f"Add to cart TimeoutError {button_locator}: {e}")

            except Exception as e:
                error(f"Add to cart error {button_locator}: {e}")

    def _check_click_add_to_cart(self, add_locator: str) -> bool:

        """Проверяет, что после клика появилась кнопка Remove"""
        try:
            remove_locator = add_locator.replace("add-to-cart", "remove")
            self.page.wait_for_selector(remove_locator, timeout=800)
            return True

        except PlaywrightTimeoutError:  # ← Меняем на PlaywrightTimeoutError
            error(f'Remove button not appeared: {remove_locator}')
            return False

        except Exception as e:
            error(f'Check add to cart failed {add_locator}: {e}')
            return False

    @allure.step("Переход в Корзину:")
    def select_to_cart(self):
        log_message('Switch to Cart:')
        try:
            button = self.page.locator(cart_button)
            self.check_expect_count(button, 1, timeout=5000, name="Cart button")

            button.scroll_into_view_if_needed()
            button.click()
            time.sleep(1)
            return True

        except LocatorNotFoundError as e:
            error(str(e))
            raise
        except PlaywrightTimeoutError:  # ← Меняем на PlaywrightTimeoutError
            error(f'Locator "{cart_button}" not found')
            return False

        except Exception as e:
            error(f'Select to cart failed for "{cart_button}": {e}')
            return False


    @allure.step("Комплексный шаг: выбор продуктов и переход в корзину")
    def select_methods(self):
        log_message("=" * 50)
        log_message(f'{'=' * 16} Modul Name:{self.__class__.__name__} {'=' * 16}')
        self.get_current_url()
        self.click_add_to_cart(locators_add_to_cart)
        self.select_to_cart()
