import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import env_config, test_data


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для запуска браузера Chrome в полноэкранном режиме
    """
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    yield driver
    driver.quit()


@allure.title("Проверка поиска товара")
def test_search_functionality(driver: webdriver.Chrome) -> None:
    """
    UI-тест: проверка поиска товара.
    Входные данные: строка поиска (test_data.SEARCH_QUERY).
    Выходные данные: список найденных элементов.
    """
    driver.get(env_config.BASE_URL)
    wait = WebDriverWait(driver, env_config.TIMEOUT)

    with allure.step("Ввод поискового запроса"):
        search_input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input.search-input, "
                                  "input.input.is-rounded"))
        )
        search_input.send_keys(test_data.SEARCH_QUERY)
        search_input.send_keys(Keys.ENTER)

    with allure.step("Проверка результатов поиска"):
        results = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".app-content"))
        )
        assert len(results) > 0, "Результаты поиска должны быть найдены"


@allure.title("Проверка появления кнопки 'Оплатить заказ'")
def test_payment_button(driver: webdriver.Chrome) -> None:
    """
    UI-тест: проверка оформления заказа.
    Входные данные: тестовые данные пользователя (test_data.TEST_USER).
    Выходные данные: наличие кнопки 'Оплатить заказ'.
    """
    wait = WebDriverWait(driver, env_config.TIMEOUT)
    driver.get(env_config.PRODUCT_URL)

    with allure.step("Добавление товара в корзину"):
        first_buy_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".button.is-fullwidth.is-medium.is-primary"))
        )
        first_buy_button.click()

    with allure.step("Переход в корзину"):
        cart_icon = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".button.is-fullwidth.is-medium.is-light"))
        )
        cart_icon.click()

    with (((allure.step("Заполнение формы заказа")))):
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#name.input"
                              ""))).send_keys(test_data.TEST_USER["name"])
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Номер "
                       "телефона']"))).send_keys(test_data.TEST_USER["phone"])
        driver.find_element(By.NAME, "contact_email") \
            .send_keys(test_data.TEST_USER["email"])
        city_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Укажите город доставки']")))
        city_input.send_keys(test_data.TEST_USER["city"])
        city_input.send_keys(Keys.ARROW_DOWN)
        city_input.send_keys(Keys.ENTER)

    with allure.step("Выбор типа доставки"):
        delivery_option = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='radio'][name='delivery_type']"))
        )
        driver.execute_script("arguments[0].click();", delivery_option)

    with allure.step("Выбор места вручения"):
        place_option = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[type='radio']"
                                  "[name='destination_type']"))
        )
        driver.execute_script("arguments[0].click();", place_option)

    with allure.step("Выбор способа оплаты"):
        payment_options = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".column.is-4")))
        payment_options[0].click()

    with allure.step("Подтверждение заказа"):
        confirm_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Подтвердить заказ')]"))
        )
        driver.execute_script("arguments[0]."
                              "scrollIntoView(true);", confirm_button)
        driver.execute_script("arguments[0].click();", confirm_button)

    with (allure.step("Проверка появления кнопки 'Оплатить заказ'")):
        pay_button = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(text(),'Оплатить заказ')]"))
        )
        assert pay_button.is_displayed() and pay_button.is_enabled(), \
            "Кнопка 'Оплатить заказ' должна быть доступна"


@allure.title("Проверка перехода по кнопке VK в хедере")
def test_vk_link_opens_group(driver: webdriver.Chrome) -> None:
    """
    UI-тест: проверка перехода по кнопке VK в хедере.
    """
    wait = WebDriverWait(driver, env_config.TIMEOUT)

    with allure.step("Открыть главную страницу сайта"):
        driver.get(env_config.BASE_URL)

    with allure.step("Нажать на кнопку VK в хедере"):
        vk_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a[href='https://vk.com/"
                                  "xlmedia_animeshop']"))
        )
        vk_button.click()

    with allure.step("Переключиться на новую вкладку и проверить URL"):
        driver.switch_to.window(driver.window_handles[-1])
        assert "vk.com/xlmedia_animeshop" in driver.current_url


@allure.title("Проверка перехода по кнопке Telegram в хедере")
def test_telegram_link_opens_group(driver: webdriver.Chrome) -> None:
    """
    UI-тест: проверка перехода по кнопке Telegram в хедере.
    """
    wait = WebDriverWait(driver, env_config.TIMEOUT)

    with allure.step("Открыть главную страницу сайта"):
        driver.get(env_config.BASE_URL)

    with allure.step("Нажать на кнопку Telegram в хедере"):
        telegram_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a[href='https://t.me/xlmedia_animeshop']"))
        )
        driver.execute_script("arguments[0].click();", telegram_button)

    with allure.step("Переключиться на новую вкладку и проверить URL"):
        driver.switch_to.window(driver.window_handles[-1])
        assert ("t.me/xlmedia_animeshop"
                "") in driver.current_url or ("telegra"
                                              "m.org") in driver.current_url


@allure.title("Проверка перехода по кнопке VK в футере")
def test_vk_footer_link_opens_group(driver: webdriver.Chrome) -> None:
    """
    UI-тест: проверка перехода по кнопке VK в футере.
    Входные данные: URL главной страницы.
    Выходные данные: открытие новой вкладки vk.com с группой XL Media.
    """
    wait = WebDriverWait(driver, env_config.TIMEOUT)

    with allure.step("Открыть главную страницу сайта"):
        driver.get(env_config.BASE_URL)

    with allure.step("Нажать на кнопку VK в футере"):
        vk_footer_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[@class='app-footer-social-item']"
                           "[img[@alt='vk']]"))
        )
        driver.execute_script("arguments[0].click();", vk_footer_button)

    with allure.step("Переключиться на новую вкладку и проверить URL"):
        driver.switch_to.window(driver.window_handles[-1])
        assert "vk.com/xlmedia_animeshop" in driver.current_url


@allure.title("Проверка перехода по кнопке Telegram в футере")
def test_telegram_footer_link_opens_group(driver: webdriver.Chrome) -> None:
    """
    UI-тест: проверка перехода по кнопке Telegram в футере.
    Входные данные: URL главной страницы.
    Выходные данные: открытие новой вкладки Telegram с возможностью выбора
    продолжения взаимодействия через приложение или web-страницу.
    """
    wait = WebDriverWait(driver, env_config.TIMEOUT)

    with allure.step("Открыть главную страницу сайта"):
        driver.get(env_config.BASE_URL)

    with allure.step("Нажать на кнопку Telegram в футере"):
        telegram_footer_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[@class='app-footer-social-item']"
                           "[img[@alt='telegram']]"))
        )
        driver.execute_script("arguments[0].click();", telegram_footer_button)

    with ((((allure.step("Переключиться на новую вкладку и проверить URL"))))):
        driver.switch_to.window(driver.window_handles[-1])
        assert ("t.me/xlmedia_"
                "animeshop") in driver.current_url or ("telegram.org"
                                                       ) in driver.current_url


@allure.title("Проверка перехода в раздел 'Манга' через каталог")
def test_catalog_manga_section(driver: webdriver.Chrome) -> None:
    """
    UI-тест: проверка перехода в раздел 'Манга' через каталог.
    Входные данные: URL главной страницы.
    Выходные данные: переход на страницу раздела 'Манга'.
    """
    wait = WebDriverWait(driver, env_config.TIMEOUT)

    with allure.step("Открыть главную страницу сайта"):
        driver.get(env_config.BASE_URL)

    with allure.step("Нажать на кнопку 'Каталог'"):
        catalog_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        ".button.is-primary."
                                        "header-catalog-button"))
        )
        driver.execute_script("arguments[0].click();", catalog_button)

    with allure.step("Нажать на раздел 'Манга'"):
        manga_section = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/manga/']"))
        )
        driver.execute_script("arguments[0].click();", manga_section)

    with allure.step("Проверить, что открылась страница раздела 'Манга'"):
        assert "manga" in driver.current_url.lower()
