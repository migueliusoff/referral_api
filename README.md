# Referral API

Тестовая задача по реализации небольшого проекта с регистрацией пользователей и реферальной системой.

Проект реализован на Django с использованием DRF для реализации RESTful API, в качестве базы данных используется PostgreSQL.
Для аутентификации используются либо JWT токены, либо OAUTH 2.0.

## Запуск проекта локально
Проект использует poetry для менеджмента зависимостей и virtualenv'ов и docker для бд.
Прежде всего нужно установить poetry - [ссылка на доку](https://poetry.eustace.io/docs/)

Далее:

1. Установка зависимостей проекта <br>`$ poetry install`
2. Активация virtualenv<br> `$ poetry shell`
3. Запуск сервисов (postgres)<br> `$ docker compose up -d`
4. Запуск миграций<br> `$ python src/manage.py migrate`
5. Запуск веб-сервера<br> `$ python src/manage.py runserver`

Для автоматического запуска линтера и форматтера
`$ pre-commit install`

Swagger находится по пути `/api/swagger/`, redoc - `/api/redoc/`
Для аутентификации в swagger необходимо получить access token по `POST /api/token/` после регистрации.
Регистрацию можно пройти по `POST /api/register/`. После получения токена нужно нажать на кнопку `Authorize` и ввести 
`Bearer your_token`, где `your_token` - полученный вами access token.