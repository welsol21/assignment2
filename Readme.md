# HR System Application

This is a distributed HR system application implemented with gRPC, RabbitMQ, and Docker. It includes a client, server, and RabbitMQ consumer service to process employee-related queries and logs system activities.

## Features

1. Employee Query System:
  * Retrieve employee salary details.
  * Fetch vacation leave entitlement and history.
  * Handle unrecognized employee IDs and invalid queries gracefully.

2. Activity Logging:
  * Logs all employee queries to a RabbitMQ message queue.
  * RabbitMQ consumer processes and stores the logs.

3. Multi-client Support:
  * The server supports multiple simultaneous clients using gRPC.

4. Dockerized Environment:
  * Fully containerized using Docker Compose.

## System Architecture

1. RabbitMQ:
  * Acts as the message broker to handle activity logs.

2. gRPC Server:
  * Processes employee queries from clients.
  * Publishes logs to RabbitMQ.

3. Client:
  * Menu-driven console application for querying the server.

4. RabbitMQ Consumer:
  * Consumes and processes activity logs from RabbitMQ.

## Prerequisites

  * Docker
  * Docker Compose

## Setup and Running the Application
  
1. Clone the repository:
```bash
git clone <repository_url>
cd <repository_name>
```

2. Build and run the services:
```bash
docker-compose up --build
```

3. Access RabbitMQ Management Interface:

  * URL: ``http://localhost:15672``
  * Default credentials: ``guest/guest``

## Testing the Application

1. When all services are up, the client application runs automatically and prompts for inputs.
2. Follow the on-screen menu to query employee details:
  * Enter valid employee IDs to fetch salary or leave details.
  * Test with invalid employee IDs or queries to observe error handling.

## Project Structure

```bash
Assignment2/ 
├── client/ # Client application 
│ ├── client.py # Client implementation 
│ ├── Dockerfile # Dockerfile for the client 
│ ├── requirements.txt # Python dependencies for the client 
│ └── wait-for-server.sh # Shell script to wait for the gRPC server to start 
├── logs/ # Logs directory 
│ ├── client.log # Log file for client operations 
│ ├── consumer.log # Log file for consumer operations
│ └── server.log # Log file for server operations
├── rabbit_consumer/ # RabbitMQ consumer application 
│ ├── consumer.py # RabbitMQ consumer implementation 
│ ├── Dockerfile # Dockerfile for the RabbitMQ consumer 
│ ├── requirements.txt # Python dependencies for the RabbitMQ consumer 
│ └── wait-for-rabbitmq-for-consumer.sh # Shell script to wait for RabbitMQ to start 
├── proto/ # Protocol Buffer definitions 
│ ├── employee.proto # Protocol Buffer schema for employee service 
├── server/ # gRPC server application 
│ ├── employee_pb2_grpc.py # Auto-generated gRPC classes 
│ ├── employee_pb2.py # Auto-generated Protocol Buffer classes 
│ ├── server.py # gRPC server implementation 
│ ├── Dockerfile # Dockerfile for the server 
│ ├── requirements.txt # Python dependencies for the server 
│ └── wait-for-rabbitmq.sh # Shell script to wait for RabbitMQ to start 
├── docker-compose.yml # Docker Compose file to orchestrate services 
├── .gitignore # Git ignore file 
└── README.md # Project documentation
```

## Notes
1. **Hardcoded Client Responses**:  
   To save time and ensure functionality, the client (`client.py`) has hardcoded inputs to simulate the assignment's predefined scenario. This provides a seamless demonstration of the expected behavior as outlined in the task description.

2. **Logging**:  
   Each component (client, server, and consumer) generates logs in its respective `logs/` directory for easier debugging and tracking of system activity.

3. **Message Queue (RabbitMQ)**:  
   RabbitMQ is used to handle logging of requests and responses, ensuring reliable message delivery.

---

## Summary
This project is a fully containerized application that:
1. Provides employee details through a gRPC server.
2. Logs activity using RabbitMQ.
3. Consumes logs with a RabbitMQ consumer.
4. Simulates client-server interactions using predefined inputs.