#!/bin/sh
set -e

echo "Waiting for MySQL at $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "MySQL is not ready yet..."
  sleep 5
done

echo "MySQL is up - executing command"
exec "$@"
