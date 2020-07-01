#! /usr/bin/env bash
set -e

python pre_start.py

export GUNICORN_CONF=${GUNICORN_CONF:-gunicorn_conf.py}
echo "Starting gunicorn"
exec gunicorn -k uvicorn.workers.UvicornWorker -c "$GUNICORN_CONF" "$APP_MODULE"
