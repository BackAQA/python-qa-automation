# Python QA Automation Framework

Самостоятельный проект по автоматизации тестирования учебного интернет-магазина [Automation Exercise](https://www.automationexercise.com/).

## Технологический стек

- **Python 3** — язык программирования.
- **Pytest** — тестовый фреймворк.
- **Playwright** — автоматизация браузера.
- **Allure Report** — формирование тестовых отчётов.
- **pytest-xdist** — поддержка параллельного выполнения тестов.
- **Git** — система контроля версий.

## О проекте

Проект представляет собой фреймворк автоматизации тестирования веб-приложения с использованием Python, Pytest и Playwright.

В основе архитектуры лежит паттерн **Page Object Model (POM)**. Логика взаимодействия со страницами и отдельными компонентами интерфейса отделена от тестовых сценариев.

Основная цель проекта — практическое применение современных подходов к UI-автоматизации, организации тестового кода и управлению тестовыми данными.

## Реализованный функционал

- Автоматизация пользовательских сценариев через Playwright Python.
- Проверка регистрации, авторизации, выхода из аккаунта и удаления пользователя.
- Тестирование каталога товаров и страниц с подробной информацией о товарах.
- Проверка добавления и удаления товаров из корзины.
- Проверка количества товаров и правильности расчёта итоговой стоимости.
- Проверка ограничений оформления заказа для неавторизованных пользователей.
- Реализация архитектуры Page Object Model (POM).
- Создание переиспользуемых UI-компонентов.
- Использование Pytest Fixtures для подготовки и очистки тестовых данных.
- Параметризация тестовых сценариев с помощью `pytest.mark.parametrize`.
- Организация тестов с помощью пользовательских Markers.
- Реализация Setup и Teardown для управления жизненным циклом тестов.
- Автоматическое создание скриншотов при падении UI-тестов.
- Интеграция скриншотов с Allure Report.
- Поддержка параллельного запуска тестов через `pytest-xdist`.

## Архитектура проекта

```text
python-qa-automation/
│
├── components/
│   ├── cart_item_component.py
│   ├── cart_modal_component.py
│   ├── checkout_modal_component.py
│   ├── header_component.py
│   └── product_card_component.py
│
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── signup_page.py
│   ├── products_page.py
│   ├── product_details_page.py
│   └── cart_page.py
│
├── tests/
│   ├── conftest.py
│   └── ui/
│       ├── test_account_lifecycle.py
│       ├── test_add_to_cart.py
│       ├── test_cart_page.py
│       ├── test_checkout.py
│       ├── test_home_page.py
│       ├── test_login.py
│       ├── test_navigation.py
│       ├── test_product_details_page.py
│       └── test_products_page.py
│
├── artifacts/
│   └── screenshots/
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com/BackAQA/python-qa-automation.git

cd python-qa-automation
```

### 2. Создание виртуального окружения

```bash
python3 -m venv .venv
```

Активация виртуального окружения на macOS:

```bash
source .venv/bin/activate
```

### 3. Установка зависимостей

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

### 4. Установка браузера Chromium

```bash
playwright install chromium
```

## Запуск тестов

Запуск всех UI-тестов:

```bash
pytest -v
```

Запуск тестов конкретного файла:

```bash
pytest -v tests/ui/test_login.py
```

Запуск отдельного теста:

```bash
pytest -v tests/ui/test_home_page.py::test_home_page_is_displayed
```

Запуск Smoke-тестов:

```bash
pytest -v -m smoke
```

Запуск Regression-тестов:

```bash
pytest -v -m regression
```

Запуск тестов по ключевому слову:

```bash
pytest -v -k login
```

Параллельный запуск в двух процессах:

```bash
pytest -v -n 2
```

## Allure Report

Формирование результатов тестирования:

```bash
pytest --alluredir=allure-results
```

Просмотр Allure-отчёта:

```bash
allure serve allure-results
```

Для запуска отчёта требуется отдельно установленный Allure Commandline.

## Скриншоты при ошибках

При падении UI-теста автоматически создаётся скриншот текущей страницы.

Скриншоты сохраняются в директории:

```text
artifacts/screenshots/
```

Изображения также прикрепляются к результатам тестирования Allure.

## Текущее состояние проекта

**Завершённый этап:** UI-автоматизация с использованием Pytest и Playwright.

**Следующие этапы развития:**

- API-автоматизация с использованием Python Requests.
- Создание общей архитектуры для UI- и API-тестирования.
- Интеграция с GitHub Actions для автоматического запуска тестов в CI/CD.