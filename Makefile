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
	python manage.py test task_manager.tests.tests_user

test-status:
	python manage.py test task_manager.tests.tests_status

test-task:
	python manage.py test task_manager.tests.tests_task