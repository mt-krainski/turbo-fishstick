#!/usr/bin/env bash

nginx

poetry run ./turbo_fishstick/manage.py migrate
poetry run ./turbo_fishstick/manage.py runserver 0.0.0.0:8000
