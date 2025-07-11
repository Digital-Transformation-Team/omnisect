#!/bin/bash

set -eu

if [ "$1" == "dbinit" ]; then
    poetry run cli dbinit
    poetry run alembic upgrade head
elif [ "$1" == 'api' ]; then
    poetry run uvicorn web.app:app --host 0.0.0.0 --port 8000 --reload
else
    exec "$@"
fi