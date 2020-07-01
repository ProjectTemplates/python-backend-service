# Base image
# Build and push to dockerhub, for other images to inherit from

FROM python:3.8-slim as base

ARG RUN_LEVEL

ENV RUN_LEVEL=${RUN_LEVEL}
ENV POETRY_VERSION=1.0.2

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on
ENV PYTHONPATH=/opt/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

RUN mkdir /opt/app
WORKDIR /opt/app

COPY deployment/pre_start.py /opt/app/

ONBUILD COPY pyproject.toml poetry.loc[k] /opt/app/
ONBUILD RUN poetry install $(test $RUN_LEVEL == production && echo "--no-dev") --no-interaction --no-ansi
