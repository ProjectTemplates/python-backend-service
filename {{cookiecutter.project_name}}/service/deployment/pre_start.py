import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

{% if cookiecutter.use_postgres == "Yes" -%}
from database import Session
{%- endif %}
{% if cookiecutter.use_mongo == "Yes" -%}
from database import Mongo
{%- endif %}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60  # 1 minute
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
{%- if cookiecutter.use_postgres == "Yes" %}
        pg = Session()
        pg.execute('SELECT 1')
{%- endif %}
{%- if cookiecutter.use_mongo == "Yes" %}
        mongo = Mongo()
        mongo.mongo_db.list_collections()
{%- endif %}
        pass
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == '__main__':
    init()
