#!/bin/sh
# wait-for-postgres.sh
# Based on https://docs.docker.com/compose/startup-order/

set -e

sleep 1

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  echo >&2 "Postgres is unavailable. Sleeping"
  sleep 1
done

echo >&2 "Postgres is up. Executing command: \"$*\""
exec "$@"
