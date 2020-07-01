# pylint: disable=C0413

from typing import Any

{% if cookiecutter.use_mongo == "Yes" -%}
from pymongo import MongoClient
{%- endif %}
{% if cookiecutter.use_postgres == "Yes" -%}
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
{%- endif %}

{% if cookiecutter.use_postgres == "Yes" -%}
from conf import PG_URI
{%- endif %}
{% if cookiecutter.use_mongo == "Yes" -%}
from conf import MONGO_URI
{%- endif %}

{% if cookiecutter.use_postgres == "Yes" -%}
SQLALCHEMY_DATABASE_URL = PG_URI
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: Any = declarative_base()

from .models import *  # isort:skip
{%- endif %}


{% if cookiecutter.use_mongo == "Yes" -%}
class Mongo:
    def __getattr__(self, item):
        return getattr(self.mongo_collection, item)

    def __init__(self, collection: Optional[str] = None):
        self.mongo_client = MongoClient(MONGO_URI)
        self.mongo_db = self.mongo_client[mongo_settings.MONGO_DEFAULT_NAME]
        if collection:
            self.mongo_collection = self.mongo_db[collection]
        else:
            self.mongo_collection = None

    def set_collection(self, collection: str):
        self.mongo_collection = collection
{%- endif %}


__all__ = [
{% if cookiecutter.use_postgres == "Yes" -%}
    'Base',
    'Session',
{%- endif %}
{% if cookiecutter.use_mongo == "Yes" -%}
    'Mongo',
{%- endif %}
]
