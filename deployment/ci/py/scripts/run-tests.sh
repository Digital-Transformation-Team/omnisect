#!/bin/bash

trap 'catch $? $LINENO' ERR

catch() {
  echo "Error $1 occurred on line $2"
  exit 1
}


set -eux
python --version

source ./deployment/ci/py/scripts/common-init.sh

pushd omnisect

poetry install --with tests,linter
ruff check .

export PYTHON_ENV=test
poetry run cli dbinit
[ -d "alembic" ] && alembic upgrade head
pytest

popd
