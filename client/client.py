import grpc
import logging
import os
import employee_pb2
import employee_pb2_grpc


log_file = os.path.join(os.path.dirname(__file__), "logs/client.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main():
    print("HR System 1.0")
    channel = grpc.insecure_channel('localhost:50051')
    stub = employee_pb2_grpc.EmployeeServiceStub(channel)

    while True:
        emp_id = input("What is the employee id? ").strip()
        if not emp_id:
            print("Exiting HR System. Goodbye!")
            break

        # Отправляем запрос на сервер с ID сотрудника
        request = employee_pb2.EmployeeRequest(employee_id=emp_id)
        try:
            response = stub.GetEmployeeDetails(request)
            print(response.message)

            # Проверяем, был ли сотрудник найден
            if "Sorry... I don’t recognise that employee id" in response.message:
                continue  # Запрашиваем новый ID
        except grpc.RpcError as e:
            print("Connection error: Unable to reach the server.")
            logging.error(f"gRPC Error: {e.code()} - {e.details()}")
            break

        # Вопросы о типе запроса
        while True:
            query_type = input("Salary (S) or Annual Leave (L) Query? ").strip().upper()
            if query_type in ["S", "L"]:
                break
            print("Invalid input. Please enter 'S' or 'L'.")

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
            year=year
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
