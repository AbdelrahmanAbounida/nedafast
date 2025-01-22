#! /usr/bin/env bash

set -e
set -x

python -c "from app import app; import json; print(json.dumps(app.app.openapi()))" > ./openapi.json