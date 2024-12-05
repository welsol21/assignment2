import grpc
from concurrent import futures
import logging
import os
import employee_pb2
import employee_pb2_grpc

# Setting up logs
log_file = os.path.join(os.path.dirname(__file__), "logs/server.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Examples of employies data
employees = {
    "E00123": {"name": "Aadya Khan", "salary": 38566, "leave_taken": {2016: 22}},
    "E01033": {"name": "John Smith", "salary": 29400, "leave_entitlement": 25, "overtime": 2587, "leave_taken": {2018: 15}},
}


class EmployeeService(employee_pb2_grpc.EmployeeServiceServicer):
    def GetEmployeeDetails(self, request, context):
        emp_id = request.employee_id
        if emp_id not in employees:
            return employee_pb2.EmployeeResponse(message="Sorry... I don’t recognise that employee id")

        emp_data = employees[emp_id]
        response_message = ""

        if request.query_type == "S":
            if request.sub_query == "C":
                response_message = f"Employee {emp_data['name']}:\nCurrent basic salary: {emp_data['salary']}"
            elif request.sub_query == "T" and request.year:
                salary = emp_data.get('salary', 0)
                overtime = emp_data.get('overtime', 0)
                response_message = (f"Employee {emp_data['name']}:\nTotal Salary for {request.year}: "
                                    f"Basic pay, {salary}; Overtime, {overtime}")
        elif request.query_type == "L":
            if request.sub_query == "C":
                if 'leave_entitlement' in emp_data:
                    response_message = (f"Employee {emp_data['name']}:\nCurrent annual leave entitlement: "
                                        f"{emp_data['leave_entitlement']} days")
                else:
                    response_message = (f"Employee {emp_data['name']}:\nCurrent annual leave entitlement is not available.")
            elif request.sub_query == "Y" and request.year in emp_data.get("leave_taken", {}):
                leave_taken = emp_data["leave_taken"][request.year]
                response_message = (f"Employee {emp_data['name']}:\nLeave taken in {request.year}: {leave_taken} days")
            elif request.sub_query == "Y":
                response_message = f"Employee {emp_data['name']}:\nNo leave data available for {request.year}."

        return employee_pb2.EmployeeResponse(message=response_message)


def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    employee_pb2_grpc.add_EmployeeServiceServicer_to_server(EmployeeService(), server)
    server_address = '[::]:50051'
    server.add_insecure_port(server_address)
    logging.info(f"Server is running on {server_address}...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    run_server()
