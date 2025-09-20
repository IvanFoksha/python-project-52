#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

make install
make collectstatic --noinput
make migrate
gunicorn task_manager.wsgi:application --bind 0.0.0.0:$PORT