# For security reasons, should be loaded from env variables in production
{% if cookiecutter.use_postgres == "Yes" -%}
PG_NAME = None
PG_USER = None
PG_PASSWORD = None
PG_HOST = None
PG_PORT = '5432'
{%- endif %}

{% if cookiecutter.use_mongo == "Yes" -%}
MONGO_DEFAULT_NAME = None
MONGO_USER = None
MONGO_PASSWORD = None
MONGO_HOST = None
MONGO_PORT = '27017'
{%- endif %}

{% if (cookiecutter.use_celery == "Yes" or cookiecutter.use_redis == "Yes") -%}
REDIS_HOST = None
REDIS_PORT = '6379'
REDIS_USER = None
REDIS_PASSWORD = None
{%- endif %}

{% if cookiecutter.use_celery == "Yes" -%}
CELERY_TASKS_DB = '14'
CELERY_RESULTS_DB = '15'
{%- endif %}

DEBUG = False
