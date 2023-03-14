# foodgram
<!-- Документация: http://superred.hopto.org/redoc/

Панель администратора: http://superred.hopto.org/admin/ -->

REST API для Foodgram, «Продуктовый помощник». 
На этом сервисе пользователи смогут публиковать рецепты, подписываться
на публикации других пользователей, добавлять понравившиеся рецепты
в список «Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

foodgram-project-react
<!-- https://github.com/<OWNER>/<REPOSITORY>/actions/workflows/<WORKFLOW_FILE>/badge.svg -->
https://github.com/elmiraz-ship-it/foodgram-project-react/actions/workflows/workflow.yml/badge.svg

### Разработчик:
```
https://github.com/Elmiraz-ship-it
```
### Технологии:
<!-- - Python 3.7
- Django 
- Django REST Framework
- Docker
- Docker-compose
- Nginx
- PostgreSQL -->
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

### Запуск контейнера фронтенда:

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/Elmiraz-ship-it/foodgram-project-react
```
Запустить проект, см документацию к проекту:

```
cd infra

docker-compose up

http://localhost/api/docs/
```
### Запуск проекта на удаленном сервере:

Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra
(cd infra):

```
scp docker-compose.yml nginx.conf username@IP:/home/username/
```

Cоздать переменные окружения в GitHub Actions в разделе Secrets > Actions

Cоздать и запустить контейнеры Docker:

```
sudo docker compose up -d
```

Выполнить миграции, собрать статику, создать суперпользователя:

```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py collectstatic --no-input
sudo docker-compose exec backend python manage.py createsuperuser
```

Наполнить БД содержимым из файла ingredients.json:

```
sudo docker compose exec backend python manage.py loaddata ingredients.json
```
