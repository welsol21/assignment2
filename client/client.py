import grpc
import logging
import os
import sys
from io import StringIO
import employee_pb2
import employee_pb2_grpc

# Настройка логирования
log_file = os.path.join(os.path.dirname(__file__), "client.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Эмуляция входных данных клиента
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

# Перенаправление стандартного ввода для автоматизации
sys.stdin = StringIO(script)


def main():
    print("HR System 1.0")
    channel = grpc.insecure_channel('grpc_server:50051')  # Подключение к gRPC серверу
    stub = employee_pb2_grpc.EmployeeServiceStub(channel)

    while True:
        emp_id = input("What is the employee id? ").strip()
        if not emp_id:
            print("Exiting HR System. Goodbye!")
            break

        # Отправляем запрос на сервер
        request = employee_pb2.EmployeeRequest(employee_id=emp_id)
        try:
            response = stub.GetEmployeeDetails(request)
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
            response = stub.GetEmployeeDetails(request)
            print(response.message)
        except grpc.RpcError as e:
            print("Connection error: Unable to process the request.")
            logging.error(f"gRPC Error: {e.code()} - {e.details()}")

        next_action = input("Would you like to continue (C) or exit (X)? ").strip().upper()
        if next_action == "X":
            print("Goodbye")
            break


if __name__ == "__main__":
    main()
