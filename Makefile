install:
	uv sync

migrate:
	python manage.py makemigrations && python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

start:
	python manage.py runserver

test-users:
	python manage.py test task_manager.users.tests

test-statuses:
	python manage.py test task_manager.statuses.tests

test-labels:
	python manage.py test task_manager.labels.tests

test-tasks:
	python manage.py test task_manager.tasks.tests

# test-all: test-users test-statuses test-tasks test-labels