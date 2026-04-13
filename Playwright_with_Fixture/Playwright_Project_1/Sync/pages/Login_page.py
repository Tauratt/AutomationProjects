import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from Playwright_with_Fixture.Playwright_Project_1.Sync.base.base_class import Settings
from Playwright_with_Fixture.Playwright_Project_1.Sync.config import (
    password_field, PASSWORD, LOGIN, login_button, login_field, Logo_catalog
)
from Playwright_with_Fixture.Playwright_Project_1.Sync.helper_func.error_class import \
    LocatorNotFoundError
from Playwright_with_Fixture.Playwright_Project_1.Sync.utilities.utils import (
    log_message, error, success, step
)


class Auth_page(Settings):
    def __init__(self, page, expect):
        super().__init__(page, expect)

    @allure.step('Ввод логина')
    def login_field(self):
        """Ввод логина"""
        log_message('Input Login:')
        try:
            field = self.page.locator(login_field)
            self.check_expect_count(field, 1, timeout=5000, name="Login Field")

            field.fill(LOGIN)
            value = field.input_value()
            assert len(value) == len(LOGIN), f"Ожидали {len(LOGIN)} символов, получили {len(value)}"
            success('\tInput Login')
            return True

        except LocatorNotFoundError as e:
            error(str(e))
            raise

        except PlaywrightTimeoutError as e:
            error(f'Login field PlaywrightTimeoutError: {e}')
            return False
        except Exception as e:
            error(f'Login field: {e}')
            return False

    @allure.step('Ввод пароля:')
    def pass_field(self):
        """Ввод пароля"""
        log_message('Input Password:')
        try:
            field = self.page.locator(password_field)
            self.check_expect_count(field, 1, timeout=5000, name="Password Field")

            field.fill(PASSWORD)
            value = field.input_value()
            assert len(value) == len(PASSWORD), f"Ожидали {len(PASSWORD)} символов, получили {len(value)}"
            success('\tInput Password')
            return True

        except LocatorNotFoundError as e:
            error(str(e))
            raise

        except PlaywrightTimeoutError as e:
            error(f'Password field TimeoutError: {e}')
            return False

        except Exception as e:
            error(f'Password field: {e}')
            return False

    @allure.step('Клик по кнопке входа')
    def click_login_button(self):
        """Клик по кнопке входа"""
        log_message('Login Button:')
        try:
            self.page.locator(login_button).click()
            step('\tClick Login Button')
            return True

        except PlaywrightTimeoutError as e:
            error(f'Login button PlaywrightTimeoutError: {e}')
            return False
        except Exception as e:
            error(f'Login button click: {e}')
            return False


    @allure.step('Проверка успешного входа')
    def check_success_login(self):
        """Проверка успешного входа"""
        log_message('Check Success Login:')
        try:
            logo = self.page.locator(Logo_catalog)
            self.expect(logo).to_have_text("Swag Labs", timeout=5000)
            success('\tSuccessful login - title Swag Labs')
            return True

        except AssertionError as e:  # ← Меняем на AssertionError
            error(f'Successful login AssertionError: {e}')
            return False
        except Exception as e:
            error(f'Successful login failed: {e}')
            return False


    @allure.step('Проверка сообщения об ошибке:')
    def check_error_message(self):
        """Проверка сообщения об ошибке"""
        step('Check Error Message:')
        try:
            error_msg = self.page.locator('[data-test="error"]')
            self.expect(error_msg).to_be_visible(timeout=5000)
            success('Сообщение об ошибке отображено')
            return True

        except AssertionError as e:
            error(f'Error message AssertionError - не найдено: {e}')
            return False
        except Exception as e:
            error(f'Сообщение об ошибке НЕ найдено: {e}')
            return False

    @allure.step('Комплексный шаг Авторизации')
    def full_authorization(self, name):
        """Полная авторизация: логин + пароль + клик"""
        log_message('=' * 50)
        log_message(f'------Браузер - {name}-----')
        log_message(f'{'=' * 16} Modul Name:{self.__class__.__name__} {'=' * 16}')
        log_message('🔐 Authorization:')

        login_ok = self.login_field()
        if not login_ok:
            return False

        pass_ok = self.pass_field()
        self.get_screenshot('auth')

        if not pass_ok:
            return False



        button_ok = self.click_login_button()
        if not button_ok:
            return False

        if self.check_success_login():
            log_message('Авторизация УСПЕШНА!')
            return True
        else:
            self.check_error_message()
            log_message('Авторизация НЕУДАЧНА!')
            return False
