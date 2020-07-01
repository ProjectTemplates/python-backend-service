#! /usr/bin/env bash
set -e

exec celery --app=worker.beat:app beat --loglevel=INFO --pidfile /tmp/celerybeat.pid -s /tmp/celerybeat-schedule
