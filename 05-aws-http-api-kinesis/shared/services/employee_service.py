from decimal import Decimal
from enum import Enum

from db_utils import DbUtils

TABLE_NAME = 'employees'

class EmployeeRole(Enum):
    MANAGER = 'manager'
    EMPLOYEE = 'employee'

class EmployeeService:
    def __init__(self) -> None:
        self.__db = DbUtils()

    def add_employee(self, 
                    given_name: str,
                    family_name: str,
                    role: str,
                    email: str):
        employee = {
            'given_name': given_name,
            'family_name': family_name,
            'role_name': role,
            'email': email
        }
        self.__db.put_item(employee, TABLE_NAME)
        return employee

    def get_by_id(self, id: str):
        return self.__db.get_item({'id': id}, TABLE_NAME)
    
    def get_all(self):
        return self.__db.scan_for_items(TABLE_NAME)

    def get_by_role(self, role: EmployeeRole):
        query = {
            'IndexName': 'employees_by_role_name',
            'KeyConditionExpression': 'role_name = :role_name',
            'ExpressionAttributeValues': {
                ':role_name': role.value
            }
        }
        return self.__db.query_for_items(query, TABLE_NAME)
    
