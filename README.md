# Selenium + Requests + Pytest + Allure Project

## Описание
Проект реализует автоматизированные **UI‑тесты** и **API‑тесты** для веб‑приложения **XL Media** (https://xlm.ru).  
Тесты разделены на два направления:
- **UI‑тесты** (Selenium) — проверка пользовательского интерфейса: поиск товаров, добавление в корзину, 
    оформление заказа, переходы по ссылкам (VK, Telegram), переход в раздел «Манга».
- **API‑тесты** (Requests) — проверка REST API: поиск товаров, добавление и удаление товара из корзины, 
    очистка корзины, негативные сценарии.

Тесты документированы с использованием **Allure** и поддерживают запуск в трёх режимах:
1. Только UI‑тесты  
2. Только API‑тесты  
3. Все тесты 

## Структура проекта
project-root/ 
├── config/ 
│ ├── __init__.py # делает папку config пакетом для удобного импорта
│ ├── env_config.py # настройки окружения (BASE_URL, таймауты и т. д.) 
│ └── test_data.py # тестовые данные (логины, id товаров, поисковые запросы) 
│ 
├── test/ 
│ ├── test_ui.py # UI-тесты (Selenium) 
│ └── test_api.py # API-тесты (Requests) 
│ 
├── requirements.txt # зависимости проекта 
├── README.md # описание проекта 
└── conftest.py # фикстуры pytest (браузер, сессия API)

## Установка
1. Клонируйте проект и перейдите в папку:
   ```bash
   git clone <repo-url>
   cd project-folder
   
2. Установите зависимости:
   pip install -r requirements.txt

3. Запуск тестов:
- Запуск только UI‑тестов: pytest test/test_ui.py --alluredir=allure-results
- Запуск только API‑тестов: pytest test/test_api.py --alluredir=allure-results
- Запуск всех тестов: pytest test/ --alluredir=allure-results

4. Для генерации отчётов используйте: allure serve allure-results

## Финальный проект
Ссылка на проект: https://katesky.yonote.ru/share/304db544-55c3-4f89-b689-0c193aec0a27
