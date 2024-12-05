#!/bin/bash

host="$1"
port="$2"

echo "Waiting for gRPC server at $host:$port..."

while ! nc -z "$host" "$port"; do
    sleep 1
done

echo "gRPC server is up and running!"

python /app/client.py
