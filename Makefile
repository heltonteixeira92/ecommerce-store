dev:
    python manage.py runserver --settings=core.settings.dev

runserver:
    python manage.py runserver --settings=core.settings.core

migrate:
    python manage.py migrate