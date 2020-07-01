# pylint: disable=W0401,C0413,W0614

import os
from typing import Optional

from pydantic import BaseSettings

APP_NAME = os.getenv('APP_NAME', 'Server')
APP_VERSION = os.getenv('APP_VERSION', '0.1.0')


class Level:
    DEV = 'dev'
    PROD = 'prod'


RUN_LEVEL = os.getenv('RUN_LEVEL', Level.PROD)

from conf.envs.prod import *  # isort: ignore

if RUN_LEVEL == Level.DEV:
    from conf.envs.dev import *  # isort: ignore


class ServiceSettings(BaseSettings):
    MAX_LIMIT: int = 20

    class Config:
        env_prefix = 'APP_'


service_settings = ServiceSettings()



{% if cookiecutter.use_celery == "Yes" -%}
class CelerySettings(BaseSettings):
    TASKS_DB: str = CELERY_TASKS_DB
    RESULT_DB: str = CELERY_RESULTS_DB

    class Config:
        env_prefix = 'APP_CELERY_'


celery_settings = CelerySettings()
{%- endif %}



{% if cookiecutter.use_postgres == "Yes" -%}
class PostgresSettings(BaseSettings):
    NAME: str = PG_NAME
    USER: str = PG_USER
    PASSWORD: str = PG_PASSWORD
    HOST: str = PG_HOST
    PORT: str = PG_PORT

    class Config:
        env_prefix = 'APP_PG_'
{%- endif %}



{% if cookiecutter.use_mongo == "Yes" -%}
class MongoSettings(BaseSettings):
    DEFAULT_NAME: str = MONGO_DEFAULT_NAME
    USER: str = MONGO_USER
    PASSWORD: str = MONGO_PASSWORD
    HOST: str = MONGO_HOST
    PORT: str = MONGO_PORT

    class Config:
        env_prefix = 'APP_MONGO_'
{%- endif %}


{% if (cookiecutter.use_celery == "Yes" or cookiecutter.use_redis == "Yes") -%}
class RedisSettings(BaseSettings):
    HOST: str = REDIS_HOST
    PORT: str = REDIS_PORT
    USER: Optional[str] = REDIS_USER
    PASSWORD: Optional[str] = REDIS_PASSWORD

    class Config:
        env_prefix = 'APP_REDIS_'
{%- endif %}


{% if cookiecutter.use_postgres == "Yes" -%}
pg_settings = PostgresSettings()
{%- endif %}
{% if (cookiecutter.use_celery == "Yes" or cookiecutter.use_redis == "Yes") -%}
redis_settings = RedisSettings()
{%- endif %}
{% if cookiecutter.use_mongo == "Yes" -%}
mongo_settings = MongoSettings()
{%- endif %}


def uri_maker(conf_object, driver):
    def make_uri(
        user: str = conf_object.USER,
        password: str = conf_object.PASSWORD,
        host: str = conf_object.HOST,
        port: str = conf_object.PORT,
        db: Optional[str] = getattr(conf_object, 'NAME', None),
    ) -> str:
        connection_string = f'{driver}://{user}:{password}@{host}:{port}'
        if db:
            connection_string += f'/{db}'
        return connection_string
    
    return make_uri


{% if cookiecutter.use_postgres == "Yes" -%}
make_pg_uri = uri_maker(pg_settings, 'postgresql+psycopg2')
{%- endif %}
{% if cookiecutter.use_mongo == "Yes" -%}
make_mongo_uri = uri_maker(mongo_settings, 'mongodb')
{%- endif %}
{% if (cookiecutter.use_celery == "Yes" or cookiecutter.use_redis == "Yes") -%}
make_redis_uri = uri_maker(redis_settings, 'redis')
{%- endif %}

{% if cookiecutter.use_postgres == "Yes" -%}
PG_URI = make_pg_uri()
{%- endif %}
{% if cookiecutter.use_mongo == "Yes" -%}
MONGO_URI = make_mongo_uri()
{%- endif %}
{% if (cookiecutter.use_celery == "Yes" or cookiecutter.use_redis == "Yes") -%}
REDIS_URL = make_redis_uri()
{%- endif %}
