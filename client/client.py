# client/client.py
import grpc
import logging
import os
import sys
from io import StringIO
import employee_pb2
import employee_pb2_grpc

log_dir = os.getenv("LOG_DIR", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "client.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ],
)

script = """\
E00123
S
C
C
W01033
E01033
S
T
2018
C
E00123
L
Y
2016
C
E01033
L
C
X
"""

sys.stdin = StringIO(script)


def main():
    logging.info("Client script started.")
    print("HR System 1.0")
    logging.info("Connecting to gRPC server at grpc_server:50051")
    channel = grpc.insecure_channel('grpc_server:50051')
    stub = employee_pb2_grpc.EmployeeServiceStub(channel)

    while True:
        emp_id = input("What is the employee id? ").strip()
        logging.info(f"User input for employee id: {emp_id}")
        if not emp_id:
            print("Exiting HR System. Goodbye!")
            logging.info("Client script terminated.")
            break

        request = employee_pb2.EmployeeRequest(employee_id=emp_id)
        try:
            logging.info(f"Sending request to server: {request}")
            response = stub.GetEmployeeDetails(request)
            logging.info(f"Received response: {response.message}")
            print(response.message)

            if "Sorry... I don’t recognise that employee id" in response.message:
                continue
        except grpc.RpcError as e:
            print("Connection error: Unable to reach the server.")
            logging.error(f"gRPC Error: {e.code()} - {e.details()}")
            break

        query_type = input("Salary (S) or Annual Leave (L) Query? ").strip().upper()

        sub_query = ""
        year = 0

        if query_type == "S":
            sub_query = input("Current salary (C) or total salary (T) for year? ").strip().upper()
            if sub_query == "T":
                year = int(input("What year? "))
        elif query_type == "L":
            sub_query = input("Current Entitlement (C) or Leave taken for year (Y)? ").strip().upper()
            if sub_query == "Y":
                year = int(input("What year? "))

        request = employee_pb2.EmployeeRequest(
            employee_id=emp_id,
            query_type=query_type,
            sub_query=sub_query,
            year=year,
        )

        try:
            logging.info(f"Sending request to server: {request}")
            response = stub.GetEmployeeDetails(request)
            logging.info(f"Received response: {response.message}")
            print(response.message)
        except grpc.RpcError as e:
            print("Connection error: Unable to process the request.")
            logging.error(f"gRPC Error: {e.code()} - {e.details()}")

        next_action = input("Would you like to continue (C) or exit (X)? ").strip().upper()
        logging.info(f"User selected next action: {next_action}")
        if next_action == "X":
            print("Goodbye")
            logging.info("Client script terminated.")
            break


if __name__ == "__main__":
    main()
