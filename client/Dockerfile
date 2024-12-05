# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy all the client code to the container
COPY ./ /app/

# Install dependencies
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait-for-server script
COPY wait-for-server.sh /usr/local/bin/wait-for-server.sh
RUN chmod +x /usr/local/bin/wait-for-server.sh

# Set the default command to wait for the server and then run the client
CMD ["bash", "/usr/local/bin/wait-for-server.sh", "grpc_server", "50051"]
