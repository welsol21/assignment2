import grpc
from generated import employee_pb2
from generated import employee_pb2_grpc


def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = employee_pb2_grpc.EmployeeServiceStub(channel)

    while True:
        emp_id = input("What is the employee id? ")
        if not emp_id:
            break
        query_type = input("Salary (S) or Annual Leave (L) Query? ")
        sub_query = input("Sub-query (e.g., 'C' for current or 'T' for total): ")
        year = int(input("Year (if applicable): ") or 0)

        request = employee_pb2.EmployeeRequest(
            employee_id=emp_id,
            query_type=query_type,
            sub_query=sub_query,
            year=year
        )
        response = stub.GetEmployeeDetails(request)
        print("Response:", response.message)

if __name__ == "__main__":
    main()
