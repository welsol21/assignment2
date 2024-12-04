import grpc
from concurrent import futures
import employee_pb2_grpc
import employee_pb2

employees = {
    "E00123": {
        "name": "Aadya Khan", 
        "salary": 38566, 
        "leave_entitlement": 25, 
        "leave_taken": {2016: 22}
        },
    "E01033": {
        "name": "John Smith", 
        "salary": 29400, 
        "overtime": 2587, 
        "leave_taken": {2018: 15}}
}


class EmployeeService(employee_pb2_grpc.EmployeeServiceServicer):
    def GetEmployeeDetails(self, request, context):
        emp_id = request.employee_id
        if emp_id not in employees:
            return employee_pb2.EmployeeResponse(message="Employee not found.")

        emp_data = employees[emp_id]
        response_message = "Invalid query."

        if request.query_type == "S":
            if request.sub_query == "C":
                response_message = f"Employee {emp_data['name']}: Current basic salary: {emp_data['salary']}"
            elif request.sub_query == "T" and request.year:
                response_message = f"Employee {emp_data['name']}: Total salary for {request.year}: Basic pay, {emp_data['salary']}; Overtime, {emp_data['overtime']}"
        elif request.query_type == "L":
            if request.sub_query == "C":
                response_message = f"Employee {emp_data['name']}: Current annual leave entitlement: {emp_data['leave_entitlement']} days"
            elif request.sub_query == "Y" and request.year in emp_data.get("leave_taken", {}):
                response_message = f"Employee {emp_data['name']}: Leave taken in {request.year}: {emp_data['leave_taken'][request.year]} days"

        return employee_pb2.EmployeeResponse(message=response_message)


def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    employee_pb2_grpc.add_EmployeeServiceServicer_to_server(EmployeeService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server is running on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    run_server()
