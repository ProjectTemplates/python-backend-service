from conf import celery_settings

from .app import app


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    pass
