#!/usr/bin/env bash

nginx

poetry run ./turbo_fishstick/manage.py collectstatic
poetry run ./turbo_fishstick/manage.py migrate
poetry run uwsgi --ini uwsgi.ini
