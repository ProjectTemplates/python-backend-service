from typing import Generator

{% if cookiecutter.use_postgres == "Yes" -%}
from database import Session
{%- endif %}
{% if cookiecutter.use_mongo == "Yes" -%}
from database import Mongo
{%- endif %}


{% if cookiecutter.use_postgres == "Yes" -%}
# FastAPI Dependency for db session management
def get_db() -> Generator[Session, None, None]:
    db = None
    try:
        db = Session()
        yield db
    finally:
        if db:
            db.close()
{%- endif %}


{% if cookiecutter.use_mongo == "Yes" -%}
def get_mongo():
    mongo = None
    try:
        mongo = Mongo()
        yield mongo
    finally:
        if mongo:
            mongo.mongo_client.close()
{%- endif %}
