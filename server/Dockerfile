# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy all application code to the container
COPY ./ /app/

# Install dependencies
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 50051

# Copy the wait script to the container
COPY wait-for-rabbitmq.sh /usr/local/bin/wait-for-rabbitmq.sh
RUN chmod +x /usr/local/bin/wait-for-rabbitmq.sh

# Use CMD to start the wait script
CMD ["/usr/local/bin/wait-for-rabbitmq.sh", "rabbitmq", "5672"]
