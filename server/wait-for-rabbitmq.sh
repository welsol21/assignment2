#!/bin/sh
# server/wait-for-rabbitmq.sh

RABBIT_HOST=$1
RABBIT_PORT=$2

echo "Waiting for RabbitMQ at ${RABBIT_HOST}:${RABBIT_PORT}..."

while ! nc -z $RABBIT_HOST $RABBIT_PORT; do
  sleep 3
done

echo "RabbitMQ is up and running!"

python /app/server.py
