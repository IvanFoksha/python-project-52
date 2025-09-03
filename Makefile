install:
	uv sync

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

start:
	python manage.py runserver

test-user:
	python manage.py test task_manager.users.tests

test-statuses:
	python manage.py test task_manager.statuses

test-labels:
	python manage.py test task_manager.labels

test-tasks:
	python manage.py test task_manager.tasks

test-filter:
	python manage.py test task_manager.tasks.tests_filters

# test-all: test-user test-statuses test-tasks test-labels test-filter