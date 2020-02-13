# pylint: disable=W0401,C0413,W0614

import os
from typing import Optional

from pydantic import BaseSettings


class Level:
    LOCAL = 'local'
    DEV = 'dev'
    PROD = 'prod'


RUN_LEVEL = os.getenv('RUN_LEVEL', Level.LOCAL)

DEBUG = False
from conf.envs.prod import *  # isort: ignore

if RUN_LEVEL in (Level.DEV, Level.LOCAL):
    from conf.envs.dev import *  # isort: ignore
if RUN_LEVEL == Level.LOCAL:
    from conf.envs.local import *  # isort: ignore


class AppSettings(BaseSettings):
    class Config:
        env_prefix = 'APP_'


# Database configuration
class DatabaseSettings(AppSettings):
    DATABASE_NAME: str = DATABASE_NAME
    DATABASE_USER: str = DATABASE_USER
    DATABASE_PASSWORD: str = DATABASE_PASSWORD
    DATABASE_HOST: str = DATABASE_HOST
    DATABASE_PORT: str = DATABASE_PORT


class ServiceSettings(AppSettings):
    MAX_LIMIT: int = 20  # for paging, remove if unused


service_settings = ServiceSettings()
db_settings = DatabaseSettings()


def make_db_uri(
    user: str = db_settings.DATABASE_USER,
    password: str = db_settings.DATABASE_PASSWORD,
    host: str = db_settings.DATABASE_HOST,
    port: str = db_settings.DATABASE_PORT,
    db: Optional[str] = db_settings.DATABASE_NAME,
) -> str:
    connection_string = f'{{cookiecutter.database_driver}}://{user}:{password}@{host}:{port}'
    if db:
        connection_string += f'/{db}'
    return connection_string


DB_URI = make_db_uri()
