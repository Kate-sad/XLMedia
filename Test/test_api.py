import pytest
import allure
import requests
import urllib.parse
from config import env_config, test_data


@pytest.fixture(scope="function")
def api_session():
    """
    Фикстура: создаёт requests.Session и закрывает после теста.
    Возвращает объект requests.Session.
    """
    session = requests.Session()
    yield session
    session.close()


@allure.title("Проверка успешного ответа API поиска товаров")
def test_search_products_status_code(api_session: requests.Session) -> None:
    """
    API-тест: проверка поиска товаров.
    Входные данные: поисковый запрос (test_data.SEARCH_QUERY).
    Выходные данные: список найденных товаров.
    """
    params = {
        "search": test_data.SEARCH_QUERY,
        "order": "desc",
        "by": "relevance",
        "page": 1,
        "prices[]": test_data.PRICES,
        "limit": test_data.LIMIT,
    }

    encoded_query = urllib.parse.quote(test_data.SEARCH_QUERY)
    headers = {
        'referer': f'https://xlm.ru/search?search={encoded_query}'
        }

    with allure.step("Отправка запроса на поиск товаров"):
        response = api_session.get(
            f"{env_config.BASE_URL}/api/search/products",
            params=params,
            headers=headers,
            timeout=env_config.TIMEOUT,
        )

    with allure.step("Проверка корректности ответа"):
        assert response.status_code == 200, \
            f"Ожидался статус 200, получено {response.status_code}"
        res = response.json()
        assert len(res["data"]) > 0, "Результаты поиска должны быть найдены"
        assert test_data.SEARCH_QUERY in res["data"][0]["name"].lower()


@allure.title("Проверка успешного добавления товара в корзину")
def test_add_product_to_basket(api_session: requests.Session) -> None:
    """
        API-тест: добавление товара в корзину.
        Входные данные: id товара (test_data.PRODUCT_ID1).
        Выходные данные: объект корзины с добавленным товаром.
    """
    body = {
        "id": test_data.PRODUCT_ID1,
        "amount": 1,
        "basket_uuid": test_data.BASKET_UUID
    }

    encoded_query = urllib.parse.quote(test_data.SEARCH_QUERY)
    headers = {
        'referer': f'https://xlm.ru/search?search={encoded_query}'
    }

    with allure.step("Отправка запроса на добавление товара"):
        response = api_session.post(
            f"{env_config.BASE_URL}/api/basket/add",
            json=body,
            headers=headers,
            timeout=env_config.TIMEOUT,
        )

    with allure.step("Проверка корректности ответа"):
        assert response.status_code in (200, 201), \
            f"Ожидался статус 200 или 201, получено {response.status_code}"
        res = response.json()
        assert res["basket_uuid"] == body["basket_uuid"]
        assert res.get("product_id") == body["id"]


@allure.title("Проверка успешного удаления товара из корзины")
def test_remove_product_from_basket(api_session: requests.Session) -> None:
    """
    API-тест: удаление товара из корзины.
    Входные данные: id товара (test_data.PRODUCT_ID1).
    Выходные данные: пустой список товаров.
    """
    body = {
        "id": test_data.PRODUCT_ID1,  # тот же product_ID1, что в Postman
        "size": None,
        "basket_uuid": test_data.BASKET_UUID
    }

    encoded_query = urllib.parse.quote(test_data.SEARCH_QUERY)
    headers = {
        'referer': f'https://xlm.ru/search?search={encoded_query}'
    }

    with allure.step("Отправка запроса на удаление товара"):
        response = api_session.post(
            f"{env_config.BASE_URL}/api/basket/remove",
            json=body,
            headers=headers,
            timeout=env_config.TIMEOUT,
        )

    with allure.step("Проверка корректности ответа"):
        assert response.status_code in (200, 201), \
            f"Ожидался статус 200 или 201, получено {response.status_code}"
        res = response.json()
        assert isinstance(res, list), f"Ожидался список, получено {type(res)}"
        assert len(res) == 0, \
            f"После удаления корзина должна быть пустой, получено {res}"


@allure.title("Проверка успешной очистки корзины")
def test_clear_basket(api_session: requests.Session) -> None:
    """
    API-тест: очистка корзины.
    Входные данные: basket_uuid (test_data.BASKET_UUID).
    Выходные данные: пустой список товаров.
    """
    body = {"basket_uuid": test_data.BASKET_UUID}

    encoded_query = urllib.parse.quote(test_data.SEARCH_QUERY)
    headers = {
        'referer': f'https://xlm.ru/search?search={encoded_query}'
    }

    with allure.step("Отправка запроса на очистку корзины"):
        response = api_session.post(
            f"{env_config.BASE_URL}/api/basket/clear",
            json=body,
            headers=headers,
            timeout=env_config.TIMEOUT,
        )

    with allure.step("Проверка корректности ответа"):
        assert response.status_code in (200, 201), \
            f"Ожидался статус 200 или 201, получено {response.status_code}"
        res = response.json()
        assert isinstance(res, list), f"Ожидался список, получено {type(res)}"
        assert len(res) == 0, \
            f"После очистки корзина должна быть пустой, получено {res}"


@allure.title("Негативный тест: очистка корзины с неверным телом запроса")
def test_clear_basket_negative(api_session: requests.Session) -> None:
    """
    API-тест: негативный сценарий очистки корзины.
    Входные данные: неверное тело запроса и метод DELETE.
    Выходные данные: ошибка 405 Method Not Allowed.
    """
    body = {
        "id": test_data.PRODUCT_ID1,
        "size": None,
        "basket_uuid": test_data.BASKET_UUID
    }

    encoded_query = urllib.parse.quote(test_data.SEARCH_QUERY)
    headers = {
        'referer': f'https://xlm.ru/search?search={encoded_query}'
    }

    with allure.step("Отправка запроса DELETE вместо POST"):
        response = api_session.delete(
            f"{env_config.BASE_URL}/api/basket/clear",
            json=body,
            headers=headers,
            timeout=env_config.TIMEOUT,
        )

    with allure.step("Проверка корректности ответа"):
        assert response.status_code == 405, \
            f"Ожидался статус 405, получено {response.status_code}"
        text = response.text.lower()
        assert "405" in text or "method not allowed" in text, (
            f"Ожидалось сообщение об ошибке 405, получено: {response.text}"
        )
