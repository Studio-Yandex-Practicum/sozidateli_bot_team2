#!/bin/bash -x

alembic upgrade head || 0

exec "$@"
