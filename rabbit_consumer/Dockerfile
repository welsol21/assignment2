# rabbit_consumer/Dockerfiel
# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy consumer code
COPY ./ /app/

# Install dependencies
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait script to the container
COPY wait-for-rabbitmq-for-consumer.sh /usr/local/bin/wait-for-rabbitmq-for-consumer.sh
RUN chmod +x /usr/local/bin/wait-for-rabbitmq-for-consumer.sh

# Use CMD to start the wait script
CMD ["/usr/local/bin/wait-for-rabbitmq-for-consumer.sh", "rabbitmq", "5672"]