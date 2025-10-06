#!/usr/bin/env sh

set -e

echo "Applying migrations ..."
alembic upgrade head
echo "Migrations applied successfully!"

exec "$@"