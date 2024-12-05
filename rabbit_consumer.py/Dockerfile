# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy consumer code
COPY ./rabbit_consumer /app/rabbit_consumer

# Install dependencies
RUN pip install pika

# Command to run the consumer
CMD ["python", "/app/rabbit_consumer/consumer.py"]
