#!/usr/bin/env bash
path_to_module=service
use_celery="{{cookiecutter.use_celery}}"
use_postgres="{{cookiecutter.use_postgres}}"

if [ "$use_celery" = "No" ]; then
    rm -rf "$path_to_module/worker"
    rm -rf "$path_to_module/deployment/celery"
    rm "$path_to_module/deployment/docker/Dockerfile.celerybeat"
    rm "$path_to_module/deployment/docker/Dockerfile.celeryd"
fi

if [ "$use_postgres" = "No" ]; then
    rm -rf "$path_to_module/database/models"
    rm -rf "$path_to_module/alembic"
    rm "$path_to_module/database/utils.py"
    rm "$path_to_module/alembic.ini"
fi

git init

cd "$path_to_module"
make format
formatting_status=$?


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo -e "\033[32mGeneration succesfull!\033[0m"
if [ $formatting_status -ne 0 ]; then
    echo "	* there were some errors during final code formatting, but don't worry about them too much"
fi
