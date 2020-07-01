# Rich template for a complete python backend service

**work in progress**

## The ultimate backend service template

Use with cookiecutter: **`cookiecutter https://github.com/ProjectTemplates/python-backend-service.git`**

Generates a foundation for a python server based on **FastAPI**, can optionally add **celery worker and celerybeat**. Uses **poetry** for dependency resolution.

*Automatically* adds dockerfiles for everything, as well as **docker-compose.yml** for development and automatic setup of all services. Also generates a simple nginx config - internal structure of the template supports creating **multiple microservices** in one repository. You can use generated nginx config and container as a *reverse proxy* to those microservices during local development.

For storage supports **MongoDB, PostgreSQL (or any other sql db with some tweaking) and Redis, or any combination of them**.

> Note: this template is a bit opinionated

---

Шаблон для бэкенд-сервиса на Python. В основе - FastAPI, опционально может добавить celery worker и celery beat. Автоматически добавляет nginx для реверс-проксирования (если микросервисов будет несколько внутри одного репозитория - структура проекта это позовляет). Для всех сервисов автоматически сконфигурируется docker-compose.yml для локальной разработки.

В качестве хранилища позволяет выбрать MongoDB, PostgreSQL, Redis, или любую комбинацию из них.
