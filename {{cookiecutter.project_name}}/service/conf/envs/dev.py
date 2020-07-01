{% if cookiecutter.use_postgres == "Yes" -%}
PG_NAME = '{{cookiecutter.project_slug}}'
PG_USER = 'user'
PG_PASSWORD = 'password'
PG_HOST = 'postgres'
{%- endif %}

{% if cookiecutter.use_mongo == "Yes" -%}
MONGO_DEFAULT_NAME = '{{cookiecutter.project_slug}}'
MONGO_USER = 'user'
MONGO_PASSWORD = 'password'
MONGO_HOST = 'mongo'
{%- endif %}

{% if (cookiecutter.use_celery == "Yes" or cookiecutter.use_redis == "Yes") -%}
REDIS_HOST = 'redis'
{%- endif %}

DEBUG = True
