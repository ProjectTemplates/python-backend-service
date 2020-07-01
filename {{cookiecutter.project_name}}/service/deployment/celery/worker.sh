#! /usr/bin/env bash
set -e

python pre_start.py

exec celery --app=worker.app:app worker --loglevel=INFO -n worker.%%h
