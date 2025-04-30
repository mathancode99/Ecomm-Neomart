#!/usr/bin/env bash
# install requirements
pip install -r requirements.txt

# run migrations
python manage.py makemigrations
python manage.py migrate

# (optional) load fixtures or create superuser (skip if not needed)
