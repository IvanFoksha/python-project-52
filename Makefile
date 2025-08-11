install:
	uv sync

migrate:
	python manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

start:
	python manage.py runserver
