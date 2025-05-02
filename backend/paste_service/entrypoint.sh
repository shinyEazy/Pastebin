#!/bin/bash
echo "Waiting for database..."
while ! nc -z db 3306; do
  sleep 1
done
echo "Database is up!"
exec "$@"