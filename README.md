# CI/CD API сервиса YaMDb

![ci/cd_api_yamdb workflow](https://github.com/LianaVolkova/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Описание проекта API Yamdb

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: "Категории", "Фильмы", "Музыка". Список категорий (Category) может быть расширен администратором. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор. Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## CI/CD

Настроен автоматический запуск тестов, обновление образа проекта на DockerHub, автоматический деплой на боевой сервер и запуск сервиса, отправка уведомления об успешном завершении workflow в Телеграм при выполнении команды push.

### Документация к API доступна по адресу [http://51.250.66.173/redoc/](http://51.250.66.173/redoc/) после запуска проекта

## Стек технологий

- Python 3.7
- Django 2.2.16
- Django REST Framework 3.12.4
- Djangorestframework-simplejwt 4.7.2
- Git
- PostgreSQL
- Docker
- Docker-compose
- Gunicorn
- Nginx
- GitHub Actions
- Выделенный сервер Linux Ubuntu 20.04 с публичным ip

### Доступный функционал

- Для аутентификации используются JWT-токены
- У неаутентифицированных пользователей доступ к API только на уровне чтения
- Создание объектов разрешено только аутентифицированным пользователям. На прочий фунционал наложено ограничение в виде административных ролей и авторства.
- Управление пользователями
- Получение списка всех категорий и жанров, добавление и удаление
- Получение списка всех произведений, их добавление. Получение, обновление и удаление конкретного произведения
- Получение списка всех отзывов, их добавление. Получение, обновление и удаление конкретного отзыва
- Получение списка всех комментариев, их добавление. Получение, обновление и удаление конкретного комментария
- Возможность получения подробной информации о себе и удаления своего аккаунта
- Фильтрация по полям

## Шаблон env-файла

Находится в файле .env.example

## Как запустить проект в dev-режиме

Склонировать репозиторий:  

```bash
git clone <название репозитория>
```

Перейти в директорию infra:  

```bash
cd yamdb_final/infra/
```  

Создать файл .env по шаблону:  

```bash
cp .env.example .env
```  

Выполнить вход на удаленный сервер

Установить docker:  

``` bash
sudo apt install docker.io
```

Установить docker-compose:

``` bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
sudo apt install docker-compose
```

или воспользоваться официальной [инструкцией](https://docs.docker.com/compose/install/)

Находясь локально в директории infra/, скопировать файлы docker-compose.yaml и nginx.conf на удаленный сервер:

```bash
scp docker-compose.yaml <username>@<host>:/home/<username>/
scp -r nginx/ <username>@<host>:/home/<username>/
```

Для правильной работы workflow необходимо добавить в Secrets данного репозитория на GitHub переменные окружения:

```bash
Переменные PostgreSQL, ключ проекта Django и их значения по-умолчанию можно взять из файла .env.example, затем установить свои.

DOCKER_USERNAME=<имя пользователя DockerHub>
DOCKER_PASSWORD=<пароль от DockerHub>
USER=<username для подключения к удаленному серверу>
HOST=<ip сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш приватный SSH-ключ>
TELEGRAM_TO=<id вашего Телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего Телеграм-бота>
```

## Workflow проекта

- **запускается при выполнении команды git push**
- **tests:** проверка кода на соответствие PEP8, запуск pytest.
- **build_and_push_to_docker_hub:** сборка и размещение образа проекта на DockerHub.
- **deploy:** автоматический деплой на боевой сервер и запуск проекта.
- **send_massage:** отправка уведомления пользователю в Телеграм.

## После успешного результата работы workflow зайти на боевой сервер

Применить миграции:  

```bash
sudo docker-compose exec web python manage.py migrate
```

Создать суперпользователя:  

```bash
sudo docker-compose exec web python manage.py createsuperuser
```

Загрузить тестовые данные:  

```bash
sudo docker-compose exec web python manage.py loaddata fixtures.json
```

## Примеры некоторых запросов API

Регистрация пользователя:

```bash
POST /api/v1/auth/signup/
```  

Получение данных своей учетной записи:

```bash
GET /api/v1/users/me/
```  

Добавление новой категории:

```bash
POST /api/v1/categories/
```  

Удаление жанра:

```bash
DELETE /api/v1/genres/{slug}
```  

Частичное обновление информации о произведении:

```bash
PATCH /api/v1/titles/{titles_id}
```  

Получение списка всех отзывов:

```bash
GET /api/v1/titles/{title_id}/reviews/
```  

Добавление комментария к отзыву:

```bash
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

### Полный список запросов API находится в документации

## Автор

- Волкова Лиана
